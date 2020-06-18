import {HTTP} from '../utils/http.js'
class GiftModel extends HTTP{

  constructor(){
    super()
    this.url_prefix = 'gift'
  }

  /**
   * 当撤消自己的赠送清单时，需要更新属性gifts显示数据，防止多次发送请求，使用以下方式该更新数据
   */ 
  update(gifts,id) {
    let trades = gifts.trades
    for(let index in trades){
      let bid = trades[index].book.id
      // 找到要撤消的书籍,让后过滤掉
      if(bid === id){
        trades.splice(index,1)
        gifts.total -= 1
        break
      }
    }
  }


  /**
   * 撤销自己的赠送清单
   * bookId:图书唯一标识
   */
  cancel(bookId){
    return this.request({
      url:`${this.url_prefix}/cancel/${bookId}`,
      method:'DELETE'
    })
  }

  /**
   * 查询自己的赠送清单
   */
  getGiftsOfSelf(){
    return this.request({
      url:this.url_prefix+'/self'
    })
  }

  /**
   * 添加至赠送清单
   * bookId:图书唯一标识
   */
  save_of_gift(bookId){
    return this.request({
      url:`${this.url_prefix}/save/${bookId}`
    })
  }

  /**
   * 获取最近上传图书
   * start:分页查询起始索引
   */
  getRecentlyUploaded(start){
    return this.request({
      url:`${this.url_prefix}/recent?start=${start}`
    })
  }

  /**
   * 获取书籍拥有者信息
   * gid:礼物唯一标识
   */
  getOccupant(gid){
    return this.request({
      url:`${this.url_prefix}/occupant/${gid}`
    })
  }

}

export {
  GiftModel
}