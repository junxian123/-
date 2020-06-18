import {HTTP} from '../utils/http.js'

class WishModel extends HTTP{
  constructor(){
    super()
    this.url_prefix = 'wish'
  }

  /**
   * 保存自己心愿
   * bookId：图书唯一标识
   */
  save_of_wish(bookId){
    return this.request({
      url: `${this.url_prefix}/${bookId}`
    })
  }

  /**
   * 获取自己心愿清单
   */
  getWishesOfSelf(){
    return this.request({
      url:this.url_prefix+'/self'
    })
  }

  /**
   * 撤销心愿
   * bookId:图书唯一标识
   */
  cancel(bookId){
    return this.request({
      url:`${this.url_prefix}/cancel/${bookId}`,
      method:'DELETE'
    })
  }

  /**
   * 当撤消自己的心愿清单时，需要更新属性wishes显示数据，防止多次发送请求，使用以下方式该更新数据
   */ 
  update(wishes, id) {
    let trades = wishes.trades
    for (let index in trades) {
      let bid = trades[index].book.id
      // 找到要撤消的书籍,让后过滤掉
      if (bid === id) {
        trades.splice(index, 1)
        wishes.total -= 1
        break
      }
    }
  }
}

export {
  WishModel
}