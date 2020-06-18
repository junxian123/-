import {HTTP} from '../utils/http.js'

class LoginModel extends HTTP{
  toLogin() {
    return new Promise((resolve,reject)=>{
      wx.login({
        // 登录成功
        success: res => {
          const code = res.code
          this._login(code).then(res => {
            wx.setStorageSync('user', res)
            resolve()
          })
        },
        fail: res => {
          wx.showToast({
            title: '登录失败',
          })
          reject()
        }
      })
    })
  }
  
  isAuthorize(){
    return new Promise((resolve,reject)=>{
      wx.getSetting({
        success:(res)=>{
          resolve(res)
        },
        fail:(res)=>{
          reject()
        }
      })
    })
  }

  checkSession(){
    wx.checkSession({
      fail:()=>{
        //session_key 已过期
        this.toLogin()
      }
    })
  }

  _login(data){
    return this.request({
      url:'token',
      data:{
        code:data
      },
      method:'POST'
    })
  }
}
export{
  LoginModel
}