import {LoginModel} from '../../models/login.js'
const loginModel = new LoginModel()
Page({

  /**
   * 页面的初始数据
   */
  data: {
    loading:false
  },
  toPrevious(event) {
    this.setData({
      loading:true
    })
    loginModel.toLogin().then(res=>{
      this.setData({ loading: false})
      wx.navigateBack({
        delta: 1
      })
    })
  }
})