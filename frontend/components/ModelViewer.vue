<template>
  <div class="model-container">
    <canvas ref="canvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
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

const emit = defineEmits(['modelHover'])

const canvas = ref(null)
let scene, camera, renderer, controls, model, raycaster, mouse
let hoveredModel = null
let models = []

const init = () => {
  // 創建場景
  scene = new THREE.Scene()
  scene.background = new THREE.Color(0x87CEEB) // 天空藍色

  // 創建相機
  const container = canvas.value.parentElement
  const width = container.clientWidth
  const height = 400
  camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000)
  camera.position.z = 3 // 調整初始相機位置，更靠近模型
  camera.position.y = 1 // 稍微提高相機高度

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

  // 添加半球光
  const hemiLight = new THREE.HemisphereLight(0xffffff, 0x444444, 3)
  scene.add(hemiLight)

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
  canvas.value.addEventListener('mouseout', onMouseOut)

  // 加載模型
  const loader = new GLTFLoader()
  loader.load(
    '/models/pokeball.glb',
    (gltf) => {
      // 創建多個模型實例
      for (let i = 0; i < props.users.length; i++) {
        const model = gltf.scene.clone()
        
        // 遍歷所有材質並設置
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
        const spacing = 3 // 寶貝球之間的間距
        const itemsPerRow = 6 // 每排的數量
        
        // 計算行和列
        const row = Math.floor(i / itemsPerRow)
        const col = i % itemsPerRow
        
        // 計算位置
        model.position.x = (col - (itemsPerRow - 1) / 2) * spacing
        model.position.z = row * spacing // 改為正數，讓新行向上排列
        model.position.y = 0
        
        model.rotation.x = Math.PI * 0.0
        model.rotation.y = Math.PI * 1.0
        model.rotation.z = Math.PI * 0.0
        
        scene.add(model)
        models.push(model)
      }
      
      // 自動調整相機位置以適應所有模型
      const box = new THREE.Box3()
      scene.traverse((object) => {
        if (object.isMesh) {
          box.expandByObject(object)
        }
      })
      const center = box.getCenter(new THREE.Vector3())
      const size = box.getSize(new THREE.Vector3())
      const maxDim = Math.max(size.x, size.y, size.z)
      const fov = camera.fov * (Math.PI / 180)
      let cameraZ = Math.abs(maxDim / 2 / Math.tan(fov / 2))
      camera.position.z = cameraZ * 1.5 // 調整為更近的距離
      camera.position.x = -0.8 // 調整水平位置
      camera.position.y = 0.6 // 調整垂直位置
      camera.lookAt(center)
      controls.target.copy(center)
    },
    undefined,
    (error) => {
      console.error('Error loading model:', error)
    }
  )

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
    // 找到被點擊的模型
    const clickedModel = intersects[0].object.parent

    if (hoveredModel !== clickedModel) {
      // 移除舊模型的發光效果
      if (hoveredModel) {
        hoveredModel.traverse((node) => {
          if (node.isMesh) {
            node.material.emissive.setHex(0x000000)
          }
        })
      }

      // 添加新模型的發光效果
      hoveredModel = clickedModel
      hoveredModel.traverse((node) => {
        if (node.isMesh) {
          node.material.emissive.setHex(0xffffff)
          node.material.emissiveIntensity = 0.5
        }
      })

      // 發送事件通知父組件
      const modelIndex = models.indexOf(hoveredModel)
      if (modelIndex !== -1) {
        emit('modelHover', props.users[modelIndex])
      }
    }
  } else if (hoveredModel) {
    // 如果滑鼠沒有懸停在任何模型上，移除發光效果
    hoveredModel.traverse((node) => {
      if (node.isMesh) {
        node.material.emissive.setHex(0x000000)
      }
    })
    hoveredModel = null
    emit('modelHover', null)
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
    emit('modelHover', null)
  }
}

onMounted(() => {
  init()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (renderer) {
    renderer.dispose()
  }
  // 移除事件監聽器
  if (canvas.value) {
    canvas.value.removeEventListener('mousemove', onMouseMove)
    canvas.value.removeEventListener('mouseout', onMouseOut)
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