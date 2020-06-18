import {config,tips} from '../config.js'
import {LoginModel} from '../models/login.js'

class HTTP{
  request({url,data,method}){
    return new Promise((resolve,reject)=>{
      this._request(url, data, resolve, reject, method)
    })
  }
  _request(url,data,resolve,reject,method='GET'){
    const access_token = wx.getStorageSync('user').access_token
    wx.request({
      url: config.url_prefix+url,
      method:method,
      data:data,
      header:{
        'content-type':'application/json',
        'Authorization':'Bearer '+ access_token
      },
      success:res=>{
        let code = res.statusCode.toString()
        console.log(res)
        if (code.startsWith('2')){
          resolve(res.data)
        }else{
          this._showToast(res.data.error_code)
          reject()
        }
      },
      fail:err=>{
        this._showToast(null)
        reject()
      }
    })
  }
  _showToast(error_code){
    if (error_code===10040||error_code===10050){
      wx.navigateTo({
        url: '/pages/login-exp/login-exp',
      })
      return
    }
    const tip = tips[error_code] || tips[1]
    wx.showToast({
      title: tip,
      mask:true,
      duration: 2000,
      icon:'none'
    })
  }
}
export {
  HTTP
}