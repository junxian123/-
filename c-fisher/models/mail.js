import {HTTP} from '../utils/http.js'

class MailModel extends HTTP{

  constructor(){
    super()
    this.url_prefix = 'mail'
  }
  getMail(){
    return this.request({
      url:this.url_prefix
    })
  }

  /**
   * 保存邮寄信息
   */
  save(nickname, mobile, province, city, address){
    return this.request({
      url:this.url_prefix+'/save',
      data:{
        nickname: nickname,
        mobile: mobile,
        province: province,
        city: city,
        address: address
      },
      method:'POST'
    })
  }
}

export {
  MailModel   
}