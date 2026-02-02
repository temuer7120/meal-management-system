App({
  onLaunch() {
    const logs = wx.getStorageSync('logs') || []
    logs.unshift(Date.now())
    wx.setStorageSync('logs', logs)
    this.initRequest()
  },
  
  initRequest() {
    wx.request({ timeout: 10000 })
  },
  
  globalData: {
    userInfo: null,
    baseUrl: 'http://localhost:5000/api',
    isAdmin: false
  },
  
  request(url, method = 'GET', data = {}) {
    return new Promise((resolve, reject) => {
      wx.request({
        url: this.globalData.baseUrl + url,
        method: method,
        data: data,
        header: {
          'Content-Type': 'application/json'
        },
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(res.data)
          } else {
            reject(res.data)
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  },
  
  uploadFile(url, filePath, name = 'file', formData = {}) {
    return new Promise((resolve, reject) => {
      wx.uploadFile({
        url: this.globalData.baseUrl + url,
        filePath: filePath,
        name: name,
        formData: formData,
        success: (res) => {
          if (res.statusCode === 200) {
            resolve(JSON.parse(res.data))
          } else {
            reject(JSON.parse(res.data))
          }
        },
        fail: (err) => {
          reject(err)
        }
      })
    })
  }
})