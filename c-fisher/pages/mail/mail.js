import {MailModel} from '../../models/mail'

const mailModel = new MailModel()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    mail:null,
    nicknameRules:{
      required: true,
      message: '昵称不能为空'
    },
    phoneRules: [{
      required: true,
      message: '手机号码不能为空'
    },{
        pattern: '/^[1]([3-9])[0-9]{9}$/',
      message:'手机号码格式不对'
    }],
    provinceRules: { 
      required: true,
      message: '省份不能为空'
    },
    cityRules: {
      required: true,
      message:'城市不能为空'
    },
    addressRules: {
      required: true,
      message:'详细地址不能为空'
    }
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    mailModel.getMail().then(res=>{
      this.setData({mail:res})
    })
  },

  onSubmit(event){
    const nickname = event.detail.value.nickname
    const mobile = event.detail.value.mobile
    const province = event.detail.value.province
    const city = event.detail.value.city
    const address = event.detail.value.address
    const isMobileError = /^[1]([3-9])[0-9]{9}$/.test(mobile)
    if (!nickname || !isMobileError||!province||!city||!address){
      this._showToast()
      return
    }else {
      mailModel.save(nickname, mobile, province, city, address).then(res=>{
        wx.navigateBack({       
          delta:1
        })
      })
    }
  },

  _showToast(){
    wx.showToast({
      title: '填写信息不全/输入信息格式错误',
      icon: 'none',
      mask: true,
      duration: 2000
    })
  }
})