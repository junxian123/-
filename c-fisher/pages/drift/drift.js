import {DriftModel} from '../../models/drift.js'

const driftModel = new DriftModel()

Page({

  /**
   * 页面的初始数据
   */
  data: {
    rDrift:null,
    sDrift:null,
  },

  onLoad: function (options) {
    
    // // 获取收到鱼漂
    this._setReceivedDriftOfMy()
  },

  onChange(event){
    const activeKey = event.detail.activeKey
    switch (activeKey){
      case 'received':this._setReceivedDriftOfMy()
      break;
      case 'sent':this._setSentDriftOfMy()
      break;
    }
  },

  onCancel(event){
    const did = event.detail.did
    driftModel.cancelDrift(did).then(res=>
      this._setReceivedDriftOfMy()
    )
  },

  onMail(event){
    const did = event.detail.did
    driftModel.mailDrift(did).then(res=>this._setSentDriftOfMy())
  },

  onReject(event){
    const did = event.detail.did
    driftModel.rejectDrift(did).then(res => this._setSentDriftOfMy())
  },

  onDelete(event){
    const did = event.detail.did
    let drift = this.data.rDrift
    driftModel.deleteDrift(did).then(res=>{
      driftModel.update(drift,did)
      this.setData({rDrift:drift})
    })
  },

  _setReceivedDriftOfMy(){
    this.setData({isShowRecived:true})
    driftModel.getReceivedDriftOfMy().then(res => 
      this.setData({
        rDrift: res
    })
  )},
  
  _setSentDriftOfMy(){
    this.setData({ isShowRecived: false })
    driftModel.getSentDriftOfMy().then(res => 
    this.setData({
      sDrift: res
    })
  )}
})