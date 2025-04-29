<template>
  <div class="model-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue'
import * as THREE from 'three'
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'

const props = defineProps({
  users: {
    type: Array,
    default: () => [],
    required: true
  }
})

const emit = defineEmits(['modelSelected'])

const canvas = ref(null)
let scene, camera, renderer, controls, raycaster, mouse
let hoveredModel = null
let selectedModel = null
let models = []
const modelLoaders = {
  normal: new GLTFLoader(),
  premium: new GLTFLoader()
}
let normalModel = null
let premiumModel = null

const loadModel = async (type) => {
  return new Promise((resolve, reject) => {
    const loader = type === 'normal' ? modelLoaders.normal : modelLoaders.premium
    const modelPath = type === 'normal' ? '/models/pokeball.glb' : '/models/premiumball.glb'
    
    loader.load(
      modelPath,
      (gltf) => {
        resolve(gltf.scene)
      },
      undefined,
      (error) => {
        console.error(`Error loading ${type} model:`, error)
        reject(error)
      }
    )
  })
}

const initModels = async () => {
  try {
    // 預先加載兩種模型
    normalModel = await loadModel('normal')
    premiumModel = await loadModel('premium')
    
    // 初始化場景中的模型
    updateModels()
  } catch (error) {
    console.error('Error initializing models:', error)
  }
}

const updateModels = () => {
  // 清除現有模型
  models.forEach(model => scene.remove(model))
  models = []
  
  // 創建新的模型實例
  props.users.forEach((user, index) => {
    const modelType = user.is_new ? 'premium' : 'normal'
    const baseModel = modelType === 'premium' ? premiumModel : normalModel
    const model = baseModel.clone()
    
    // 設置材質
    model.traverse((node) => {
      if (node.isMesh) {
        if (node.material) {
          const material = new THREE.MeshStandardMaterial()
          if (node.material.map) material.map = node.material.map
          if (node.material.color) material.color = node.material.color
          material.emissive = new THREE.Color(0x000000)
          material.emissiveIntensity = 0
          node.material = material
          node.material.needsUpdate = true
        }
      }
    })
    
    // 設置位置和旋轉
    const spacing = 3
    const itemsPerRow = 6
    const row = Math.floor(index / itemsPerRow)
    const col = index % itemsPerRow
    
    model.position.x = (col - (itemsPerRow - 1) / 2) * spacing
    model.position.z = row * spacing
    model.position.y = 0
    
    model.rotation.x = Math.PI * 0.0
    model.rotation.y = Math.PI * 1.0
    model.rotation.z = Math.PI * 0.0
    
    scene.add(model)
    models.push(model)
  })
}

const init = () => {
  // 創建場景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x87CEEB) // 天空藍色

  // 創建相機
  const container = canvas.value.parentElement
  const width = container.clientWidth
  const height = container.clientHeight
  camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000)
  
  // 計算相機位置
  const distance = 20 // 5個寶貝球的大小
  const angleZ = 20 * (Math.PI / 180) // 與Z軸的夾角
  const angleX = 70 * (Math.PI / 180) // 與X軸的夾角
  
  // 計算相機位置
  camera.position.x = 0 // X=0平面
  camera.position.y = distance * Math.sin(angleX) // Y座標
  camera.position.z = distance * Math.cos(angleZ) + 10 // Z座標
  
  // 讓相機看向原點
  camera.lookAt(new THREE.Vector3(0, 0, 0))

  // 創建渲染器
  renderer = new THREE.WebGLRenderer({ canvas: canvas.value, antialias: true })
  renderer.setSize(width, height)
  renderer.setPixelRatio(window.devicePixelRatio)
  
  // 開啟物理光照
  renderer.physicallyCorrectLights = true
  renderer.toneMapping = THREE.ACESFilmicToneMapping
  renderer.toneMappingExposure = 1.5
  renderer.outputEncoding = THREE.sRGBEncoding

  // 添加地面
  const groundGeometry = new THREE.PlaneGeometry(1000, 1000, 100, 100)
  const groundMaterial = new THREE.MeshStandardMaterial({ 
    color: 0xD2B48C,
    roughness: 0.8,
    metalness: 0.2,
    side: THREE.DoubleSide
  })
  const ground = new THREE.Mesh(groundGeometry, groundMaterial)
  ground.rotation.x = -Math.PI / 2
  ground.position.y = -2
  scene.add(ground)

  // 添加座標軸輔助器
  // const axesHelper = new THREE.AxesHelper(10)
  // scene.add(axesHelper)

  // 添加霧效果
  scene.fog = new THREE.FogExp2(0x87CEEB, 0.002)

  // 添加軌道控制器
  controls = new OrbitControls(camera, renderer.domElement)
  controls.enableDamping = false
  controls.dampingFactor = 0.05
  controls.screenSpacePanning = true
  controls.minDistance = 1
  controls.maxDistance = 100
  controls.minPolarAngle = 0 // 限制最小極角為 0 度
  controls.maxPolarAngle = Math.PI / 2 // 限制最大極角為 90 度
  controls.minAzimuthAngle = -Math.PI / 2 // 限制最小水平旋轉角度
  controls.maxAzimuthAngle = Math.PI / 2 // 限制最大水平旋轉角度
  controls.enablePan = true // 啟用平移
  controls.panSpeed = 1.0 // 設置平移速度

  // 添加光源
  const ambientLight = new THREE.AmbientLight(0xffffff, 2)
  scene.add(ambientLight)

  // 主要打光
  const mainLight = new THREE.DirectionalLight(0xffffff, 3)
  mainLight.position.set(5, 5, 5)
  scene.add(mainLight)

  // 補光1 - 從側面打光
  const fillLight1 = new THREE.DirectionalLight(0xffffff, 3)
  fillLight1.position.set(-5, 0, 5)
  scene.add(fillLight1)

  // 補光2 - 從下方打光
  const fillLight2 = new THREE.DirectionalLight(0xffffff, 3)
  fillLight2.position.set(0, -5, 0)
  scene.add(fillLight2)

  // 添加環境光貼圖
  const envMapLoader = new THREE.CubeTextureLoader()
  envMapLoader.setPath('/textures/')
  const envMap = envMapLoader.load([
    'px.jpg', 'nx.jpg',
    'py.jpg', 'ny.jpg',
    'pz.jpg', 'nz.jpg'
  ])
  scene.environment = envMap

  // 初始化光線投射器和滑鼠位置
  raycaster = new THREE.Raycaster()
  mouse = new THREE.Vector2()

  // 添加滑鼠移動事件監聽器
  canvas.value.addEventListener('mousemove', onMouseMove)
  // canvas.value.addEventListener('mouseout', onMouseOut)

  // 初始化模型
  initModels()

  // 動畫循環
  const animate = () => {
    requestAnimationFrame(animate)
    controls.update()
    renderer.render(scene, camera)
  }
  animate()
}

const handleResize = () => {
  if (renderer) {
    const container = canvas.value.parentElement
    const width = container.clientWidth
    const height = 400
    
    renderer.setSize(width, height)
    camera.aspect = width / height
    camera.updateProjectionMatrix()
  }
}

// 滑鼠點擊事件處理
const onMouseClick = (event) => {
  // 計算滑鼠在畫布上的相對位置
  const rect = canvas.value.getBoundingClientRect()
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1

  // 更新光線投射器
  raycaster.setFromCamera(mouse, camera)

  // 檢查是否與任何模型相交
  const intersects = raycaster.intersectObjects(models, true)

  if (intersects.length > 0) {
    // 找到被點擊的模型
    const clickedModel = intersects[0].object.parent

    // 如果點擊的是已選中的模型，則取消選中
    if (selectedModel === clickedModel) {
      selectedModel.traverse((node) => {
        if (node.isMesh) {
          node.material.emissive.setHex(0x000000)
        }
      })
      selectedModel = null
    } else {
      // 移除舊選中模型的發光效果
      if (selectedModel) {
        selectedModel.traverse((node) => {
          if (node.isMesh) {
            node.material.emissive.setHex(0x000000)
          }
        })
      }

      // 添加新選中模型的發光效果
      selectedModel = clickedModel
      selectedModel.traverse((node) => {
        if (node.isMesh) {
          node.material.emissive.setHex(0xffff00)
          node.material.emissiveIntensity = 0.5
        }
      })
    }

    // 發送事件通知父組件
    const modelIndex = models.indexOf(selectedModel)
    if (modelIndex !== -1) {
      emit('modelSelected', props.users[modelIndex])
    } else {
      emit('modelSelected', null)
    }
  }
}

// 滑鼠移動事件處理
const onMouseMove = (event) => {
  // 計算滑鼠在畫布上的相對位置
  const rect = canvas.value.getBoundingClientRect()
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1

  // 更新光線投射器
  raycaster.setFromCamera(mouse, camera)

  // 檢查是否與任何模型相交
  const intersects = raycaster.intersectObjects(models, true)

  if (intersects.length > 0) {
    // 找到被懸停的模型
    const hovered = intersects[0].object.parent

    // 如果當前懸停的模型不是之前懸停的模型，且不是已選中的模型
    if (hoveredModel !== hovered && hovered !== selectedModel) {
      // 移除舊模型的發光效果
      if (hoveredModel && hoveredModel !== selectedModel) {
        hoveredModel.traverse((node) => {
          if (node.isMesh) {
            node.material.emissive.setHex(0x000000)
          }
        })
      }

      // 添加新模型的發光效果
      hoveredModel = hovered
      hoveredModel.traverse((node) => {
        if (node.isMesh) {
          node.material.emissive.setHex(0xffffff)
          node.material.emissiveIntensity = 0.5
        }
      })
    }
  } else if (hoveredModel && hoveredModel !== selectedModel) {
    // 如果滑鼠沒有懸停在任何模型上，且當前懸停的模型不是已選中的模型
    hoveredModel.traverse((node) => {
      if (node.isMesh) {
        node.material.emissive.setHex(0x000000)
      }
    })
    hoveredModel = null
  }
}

// 滑鼠離開畫布事件處理
const onMouseOut = () => {
  if (hoveredModel) {
    hoveredModel.traverse((node) => {
      if (node.isMesh) {
        node.material.emissive.setHex(0x000000)
      }
    })
    hoveredModel = null
    emit('modelSelected', null)
  }
}

// 監聽 users 的變化
watch(() => props.users, () => {
  if (normalModel && premiumModel) {
    updateModels()
  }
}, { deep: true })

onMounted(() => {
  init()
  window.addEventListener('resize', handleResize)
  canvas.value.addEventListener('click', onMouseClick)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (renderer) {
    renderer.dispose()
  }
  // 移除事件監聽器
  if (canvas.value) {
    canvas.value.removeEventListener('mousemove', onMouseMove)
    // canvas.value.removeEventListener('mouseout', onMouseOut)
    canvas.value.removeEventListener('click', onMouseClick)
  }
})
</script>

<style scoped>
.model-container {
  width: 100%;
  height: 400px;
  margin-bottom: 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #f0f0f0;
  border-radius: 8px;
  overflow: hidden;
  position: relative;
}

canvas {
  width: 100%;
  height: 100%;
}
</style> 