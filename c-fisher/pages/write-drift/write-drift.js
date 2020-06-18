import {DriftModel} from '../../models/drift.js'
import {UserModel} from '../../models/user.js'
import {GiftModel} from '../../models/gift.js'
import {MailModel} from '../../models/mail.js'
import {BookModel} from '../../models/book.js'
import {DriftViewModel} from '../../view_models/drift.js'

const driftModel = new DriftModel()
const userModel = new UserModel()
const giftModel = new GiftModel()
const mailModel = new MailModel()
const bookModel = new BookModel()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    beans: 0,   // 鱼豆
    occupant: null, // 拥有者
    mail: null,  // 邮寄
    book:null,
    message:null, // 留言
    giftId:null,
    driftId:null,

    isDisabled:true,
    isShowMessage: false,
    status:false
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function (options) {
    const gid = options.giftId // 鱼漂存在时
    const bid = options.bookId
    const did = options.driftId
    this.data.giftId = gid
    this.data.driftId = did

    const user = userModel.getBeans()
    const occupant = giftModel.getOccupant(gid)
    const book = bookModel.getBook(bid)
    Promise.all([user,occupant,book]).then(res=>{
        this.setData({
          beans:res[0],
          occupant:res[1],
          book:res[2],
          isDisabled:false,
          status:res[0]>=1?false:true
        })
    })
  },

  onShow:function(){
    mailModel.getMail().then(res=>{
      console.log(res)
      this.setData({mail:res})
    })
  },

  onDrift(event){
    const mail = this.data.mail
    if (!mail) {
      wx.lin.showMessage({
        type:'warning',
        duration:3000,
        icon:'waring',
        content: '请完善邮寄信息!!!'
      })
      return
    }

    const book = this.data.book
    const giftId = this.data.giftId
    const driftId = this.data.driftId
    const message = this.data.message
    const driftViewModel = new DriftViewModel({
    book:book,mail:mail,giftId:giftId,driftId:driftId,message:message})
    driftModel.sendDriftOfRequest(driftViewModel).then(res=>{
      wx.navigateBack({
        delta: 1
      })
    })
  },

  onMessage(event){
    this.data.message = event.detail.detail.value
  },

  toPrevious(){
    wx.switchTab({
      url: '/pages/index/index',
    })
  },

})