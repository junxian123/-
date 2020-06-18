import {HTTP} from '../utils/http.js'

class UserModel extends HTTP{
  constructor(){
    super()
    this.url_prefix = 'user'
  }

  /**
   * 保存用户信息
   * nickname:微信昵称
   */
  saveUserInfo(nickname){
    return this.request({
      url:this.url_prefix+'/save',
      data: {
        nickname:nickname,
      },
      method:'POST'
    })
  }
  
  /**
   * 获取用户鱼豆
   */
  	getBeans(){
		return this.request({
		url:this.url_prefix+'/beans'
		})
  	}

	getCount() {
		return this.request({
			url: this.url_prefix + '/count'
		})
	}
}

export {
  UserModel
}