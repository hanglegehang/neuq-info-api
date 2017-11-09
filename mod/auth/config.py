# coding:utf-8
# Created by lihang on 2017/3/23.

HEADER = "User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
# 教务系统主页
INDEX_URL1 = "http://202.206.20.180/jwglxt/xtgl/login_slogin.html"
# 获取公钥地址
PUBLIC_KEY_URL2 = "http://202.206.20.180/jwglxt/xtgl/login_getPublicKey.html"
# 验证账号密码
CHECK_USER_USER = "http://202.206.20.180/jwglxt/xtgl/login_slogin.html"
TIME_OUT = 8

'''
{
  "card_number":"07302590", //校园账号，一般是学号，必填
  "name":"张三丰", //学生姓名，必填
  "gender": "男", // 性别：男/女
  "head_image": "http://xxx/xx.png"  // 学生头像地址
  "grade":"2016", //年级，学生必填
  "college":"信息科学与技术学院", //学院，学生必填
  "profession":"计算机系", // 专业，学生必填
  "class":"软件1班", // 班级
  "identity_type":1, // 身份类型：0-其他；1-学生；4-教职工；5-校友
  "identity_title": "学生", // 职称: "讲师"、“研究生”、“教授”
  "id_card":"4XXX***7", // 身份证号码
  "telephone":"137***8" // 手机号
}
,
{
    "card_number":"3109005843",
    "password":"helloworld",
    "app_key":APP_KEY,
    "nonce_str":"",(32位随机字符串)
    "timestamp":"",(时间戳)
    "sign":"9A0A8659F005D6984697E2CA0A9CF3B7"//签名
}
{
    "raw_data":"20864091e31fa8a0a56f3748798de919fd604691e95cc542202614af9521a6122f4869701bfd1cff5bb311a8b5f2853cc9a228de5d40f3d71f70dbd1f618b88e2c4a3d4a7139ce7ba9ba14947df3939aa45b1384382c8b46fdf7dcca4524c4aee773304b1c9474265661f82f6c975fca7c2a419c62ffe42670696877d9a57393f3547a5c48fdc570044324b29e4d7a35393a56b0202cad76104ef81f52508738aaee1314f1ea83d9d5cb306a1846bbd2",
    "app_key":"APP_KEY"
}
'''