import {HTTP} from '../utils/http.js'

class DriftModel extends HTTP {
  constructor(){
    super()
    this.url_prefix = 'drift'
  }

  /**
   *  赠送此书->发送鱼漂方式
   *  drift:保存鱼漂信息
   */
  sendDriftOfGift(drift){
    return this.request({
      url:this.url_prefix+'/gift',
      data:drift,
      method:'POST'
    })
  }

  /**
   * 请求此书->发送鱼漂方式
   * drift:保存鱼漂信息
   */
  sendDriftOfRequest(drift){
    return this.request({
      url: this.url_prefix + '/request',
      data: drift,
      method:'POST'
    })
  }

  /**
   * 查询自己收到的鱼漂
   */
  getReceivedDriftOfMy(){
    return this.request({
      url:this.url_prefix + '/my/received'
    })
  }

  /**
   * 查询自己送出去的鱼漂
   */
  getSentDriftOfMy() {
    return this.request({
      url: this.url_prefix + '/my/sent'
    })
  }

  /**
   * 撤消鱼漂
   * did:鱼漂唯一标识
   */
  cancelDrift(did){
    return this.request({
      url:`${this.url_prefix}/cancel/${did}`
    })
  }

  /**
   * 邮寄图书
   * did：鱼漂唯一标识
   */
  mailDrift(did){
    return this.request({
      url:`${this.url_prefix}/mail/${did}`
    })
  }

  /**
   * 拒绝鱼漂
   * did：鱼漂唯一标识
   */
  rejectDrift(did){
    return this.request({
      url:`${this.url_prefix}/reject/${did}`
    })
  }

  /**
   * 删除鱼漂
   * did：鱼漂唯一标识
   */
  deleteDrift(did){
    return this.request({
      url:`${this.url_prefix}/delete/${did}`
    })
  }

  /**
   *  删除鱼漂后，需要更新drift数据，防止多次请求，使用以下方式处理数据
   */
  update(drift, did){
    for(let index in drift){
      let id = drift[index].id
      // 找到要删除的鱼漂
      if(id === did){
        drift.splice(index,1)
        break
      }
    }
  }

   countGifted() {
	  return this.request({
		  url: `${this.url_prefix}/count_gift`
	  })
  }

}

export {
  DriftModel
}