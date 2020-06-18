
import {
    LoginModel
} from '../../models/login.js'
import {
    UserModel
} from '../../models/user.js'
import {
    MailModel
} from '../../models/mail.js'
import {
    DriftModel
} from '../../models/drift.js'

const loginModel = new LoginModel()
const userModel = new UserModel()
const mailModel = new MailModel()
const driftModel = new DriftModel()




Page({

    /**
     * 页面的初始数据
     */
    data: {
        openData: false,
        mail: null,
        beans: 0,
        receiveCount: 0,
        sendCount: 0,
    },

    /**
     * 生命周期函数--监听页面加载
     */
    onLoad: function(options) {
        loginModel.isAuthorize().then(res => {
            if (res.authSetting['scope.userInfo']) {
                this._setOpenDataT()
            } else {
                this._setOpenDataF()
            }
        })

        userModel.getCount().then(res => {
            this.setData({
                receiveCount: res.receive_count,
                sendCount: res.send_count
            })
        })

        driftModel.countGifted().then(res => {
			console.log(res)
        })
    },

    onShow(event) {
        mailModel.getMail().then(res => {
            this.setData({
                mail: res
            })
            return userModel.getBeans()
        }).then(res => this.setData({
            beans: res
        }))
    },

    getUserInfo(event) {
        // 同意授权才发送请求
        loginModel.isAuthorize().then(res => {
            //同意授权
            if (res.authSetting['scope.userInfo']) {
                this._setOpenDataT()
                const nickName = event.detail.userInfo.nickName
                userModel.saveUserInfo(nickName)
            } else {
                //拒绝授权
                this._setOpenDataF()
            }
        })
    },

    onAbout(event) {
        wx.navigateTo({
            url: '/pages/about/about',
        })
    },

    onThank(event) {
        wx.navigateTo({
            url: '/pages/thank/thank',
        })
    },

    _setOpenDataT() {
        this.setData({
            openData: true
        })
    },

    _setOpenDataF() {
        this.setData({
            openData: false
        })
    }
})