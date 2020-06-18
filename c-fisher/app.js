import {LoginModel} from '/models/login.js'
const loginModel = new LoginModel()
App({
  onLaunch:function(){
    loginModel.toLogin()
  }
})