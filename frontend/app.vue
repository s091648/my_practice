<template>
  <UContainer>
    <UCard>
      <template #header>
        <div class="flex justify-between items-center">
          <div class="flex flex-col">
            <h2> {{ commandName }}</h2>
            <p class="text-[10px] text-gray-500 mt-1">語音辨識: {{ responseCommand }}</p>
          </div>
          <div class="flex gap-2">
            <div class="relative border border-gray-300 dark:border-gray-700 rounded-lg p-1">
              <UButton
                icon="i-heroicons-document-arrow-up"
                color="gray"
                variant="soft"
                class="cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-800 transition-colors"
              >
                上傳 CSV
              </UButton>
              <UInput
                type="file"
                accept=".csv"
                @change="handleFileUpload"
                class="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              />
            </div>
            <UButton
              :icon="isRecording ? 'i-heroicons-stop' : 'i-heroicons-microphone'"
              :color="isRecording ? 'bg-red-500' : 'primary'"
              @click="toggleRecording"
              :disabled="isLoading"
              class="cursor-pointer"
              :class="{ 'bg-red-500': isRecording }"
            >
              {{ isRecording ? '停止錄音' : '開始錄音' }}
            </UButton>
          </div>
        </div>
      </template>
      
      <div v-if="users.length > 0" class="grid grid-cols-12 gap-4">
        <div class="col-span-9">
          <ModelViewer :users="users" @modelSelected="handleModelSelected" />
        </div>
        <div class="col-span-3">
          <UCard v-if="selectedUser" class="sticky top-4">
            <template #header>
              <h3 class="text-lg font-semibold">用戶詳情</h3>
            </template>
            <UTable
              :data="[selectedUser]"
              :columns="detailColumns"
              class="w-full"
            />
            <div class="flex justify-end mt-4 cursor-pointer">
              <UButton
                variant="solid"
                @click="handleDeleteSelectedUser"
                :loading="isLoading"
                class="cursor-pointer bg-red-500"
                icon="i-heroicons-trash"
              >
                刪除選定用戶
              </UButton>
            </div>
          </UCard>
        </div>
      </div>
      
      <UTable
        v-if="users.length > 0"
        :data="users"
        :columns="columns"
        :loading="loading"
        loading-color="primary"
        class="w-full mt-4"
      >
        <template #empty-state>
          <div class="flex flex-col items-center justify-center py-6 gap-3">
            <p class="text-gray-500">沒有找到使用者資料</p>
          </div>
        </template>
      </UTable>
    </UCard>

    <UOverlay
      v-if="isLoading"
      :blur="5"
      class="fixed inset-0 z-50 flex items-center justify-center bg-white/200 backdrop-blur-sm"
    >
      <div class="flex flex-col items-center gap-4">
        <ULoadingIcon
          size="xl"
          color="primary"
        />
        <p class="text-lg font-medium text-gray-900 dark:text-white">
          正在處理您的請求...
        </p>
      </div>
    </UOverlay>
  </UContainer>
</template>

<script setup>
import { ref } from 'vue'
import ModelViewer from './components/ModelViewer.vue'

const commandName = ref('請使用錄音功能與資料庫互動')
const responseCommand = ref('')
const loading = ref(false)
const users = ref([])
const isRecording = ref(false)
const mediaRecorder = ref(null)
const audioChunks = ref([])
const selectedUser = ref(null)
const isLoading = ref(false)

const columns = [
  {
    accessorKey: 'id',
    cell: ({ row }) => row.original.id,
    header: 'ID'
  },
  {
    accessorKey: 'name',
    cell: ({ row }) => row.original.name,
    header: '姓名'
  },
  {
    accessorKey: 'age',
    cell: ({ row }) => row.original.age,
    header: '年齡'
  }
]

const detailColumns = [
  {
    accessorKey: 'id',
    header: 'ID'
  },
  {
    accessorKey: 'name',
    header: '姓名'
  },
  {
    accessorKey: 'age',
    header: '年齡'
  }
]

const toggleRecording = async () => {
  if (!isRecording.value) {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorder.value = new MediaRecorder(stream)
      audioChunks.value = []

      mediaRecorder.value.ondataavailable = (event) => {
        audioChunks.value.push(event.data)
      }

      mediaRecorder.value.onstop = async () => {
        const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' })
        await transcribeAudio(audioBlob)
      }

      mediaRecorder.value.start()
      isRecording.value = true
    } catch (error) {
      console.error('Error accessing microphone:', error)
    }
  } else {
    mediaRecorder.value.stop()
    mediaRecorder.value.stream.getTracks().forEach(track => track.stop())
    isRecording.value = false
  }
}

const transcribeAudio = async (audioBlob) => {
  try {
    const formData = new FormData()
    formData.append('file', audioBlob, 'audio.wav')
    formData.append('model', 'whisper-1')

    const response = await fetch('/api/v1/transcribe', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('語音辨識失敗')
    }

    const { text } = await response.json()
    responseCommand.value = text
    await executeCommand(text)
  } catch (error) {
    console.error('Error transcribing audio:', error)
  }
}

const executeCommand = async (text) => {
  try {
    isLoading.value = true
    const formData = new FormData()
    formData.append('text', text)
    if (selectedUser.value) {
      formData.append('selectedName', selectedUser.value.name)
      formData.append('selectedAge', selectedUser.value.age)
    }

    const response = await fetch('/api/v1/execute_command', {
      method: 'POST',
      body: formData
    })

    const result = await response.json()
    
    if (!response.ok) {
      // 處理錯誤情況
      commandName.value = `錯誤: ${result.error} (辨識文字: ${result.command})`
      responseCommand.value = result.command
      throw new Error(result.error)
    }
    
    // 根據不同的 action 處理回應
    switch (result.action) {
      case 'get_all_users':
        commandName.value = '顯示所有用戶'
        await fetchUsers()
        break
      case 'get_added_user':
        commandName.value = '顯示已添加的用戶'
        await fetchUsers()
        break
      case 'create_user':
        commandName.value = '創建用戶'
        await fetchUsers()
        break
      case 'delete_user':
        commandName.value = '刪除用戶'
        selectedUser.value = null
        await fetchUsers()
        break
      case 'delete_user_by_name':
        commandName.value = '刪除用戶'
        await fetchUsers()
        break
      case 'calc_average_age':
        commandName.value = '計算平均年齡'
        console.log('平均年齡:', result.data)
        break
      default:
        commandName.value = '未知的操作'
        console.log('未知的操作:', result.action)
    }
  } catch (error) {
    console.error('Error executing command:', error)
  } finally {
    isLoading.value = false
  }
}

// 封裝獲取用戶列表的函數
const fetchUsers = async () => {
  try {
    const usersResponse = await fetch('/api/v1/get_all_users')
    const usersResult = await usersResponse.json()
    if (usersResponse.ok) {
      users.value = usersResult.map((user, index) => ({
        id: index + 1,
        name: user.Name || user.name || '',
        age: user.Age || user.age || '',
        is_new: user.is_new
      }))
    }
  } catch (error) {
    console.error('Error fetching users:', error)
  }
}

const handleModelSelected = (user) => {
  selectedUser.value = user
}

const handleFileUpload = async (event) => {
  const file = event.target.files[0]
  if (!file) return

  try {
    isLoading.value = true
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('/api/v1/add_multiple_users_from_csv', {
      method: 'POST',
      body: formData
    })

    const result = await response.json()
    if (!response.ok) {
      throw new Error(result.error || '上傳失敗')
    }

    commandName.value = '批量添加用戶'
    responseCommand.value = '用戶已成功添加'
    
    // 更新用戶列表
    await fetchUsers()
  } catch (error) {
    console.error('Error uploading file:', error)
    commandName.value = `錯誤: ${error.message}`
    responseCommand.value = '請檢查 CSV 檔案格式是否正確'
  } finally {
    isLoading.value = false
    // 清空檔案輸入
    event.target.value = ''
  }
}

const handleDeleteSelectedUser = async () => {
  if (!selectedUser.value) return
  
  try {
    isLoading.value = true
    const formData = new FormData()
    formData.append('selectedName', selectedUser.value.name)
    formData.append('selectedAge', selectedUser.value.age)

    const response = await fetch('/api/v1/delete_user', {
      method: 'POST',
      body: formData
    })

    if (!response.ok) {
      throw new Error('刪除用戶失敗')
    }

    commandName.value = '刪除用戶'
    selectedUser.value = null
    await fetchUsers()
  } catch (error) {
    console.error('Error deleting user:', error)
    commandName.value = `錯誤: ${error.message}`
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}
</style>
