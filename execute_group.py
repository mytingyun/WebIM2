#coding: utf-8

from selenium import webdriver
import time,sys,requests
from config import *
from chat_group import ChatGroup
import unittest
sys.path.append("..")

deluser(user1)
deluser(user2)
deluser(user3)

class TestGroupChat(unittest.TestCase):
    def setUp(self):
        self.driver3 = webdriver.Chrome()
        self.threeuser = ChatGroup(self.driver3, user3, gpasswd, url, user1, groupname)
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')
        self.browser = webdriver.Chrome(chrome_options=options)
        self.twouser = ChatGroup(self.browser, user2, gpasswd, url, user1, groupname)
        driver1 = webdriver.Chrome()
        self.oneuser = ChatGroup(driver1, user1, gpasswd, url, user2, groupname)


    def testPublicGroupNo(self):
        u'验证创建群组'
        self.oneuser.sign_in()
        self.twouser.sign_in()
        self.threeuser.sign_in()
        self.oneuser.login()
        self.assertTrue(self.oneuser.publicgroup(), True)
        self.oneuser.quitBrowser()
        self.twouser.quitBrowser()
        self.threeuser.quitBrowser()
    def testInviteMember(self):
        u'验证邀请其他人员加入群聊'
        self.oneuser.login()
        self.assertTrue(self.oneuser.invitemember(user2), True)
        time.sleep(2)
        self.oneuser.quitBrowser()
        self.twouser.quitBrowser()
        self.threeuser.quitBrowser()
    def testVerifyJoin(self):
        u'验证是否加入成功'
        self.twouser.login()
        global groupnum
        self.judge, groupnum = self.twouser.verifyjoin()
        self.assertTrue(self.judge, True)
        self.twouser.quitBrowser()
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
    def testApplyGroup(self):
        u'验证申请加入群聊'
        self.threeuser.login()
        self.assertTrue(self.threeuser.applyjoin(groupnum), True)
        self.twouser.quitBrowser()
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
    def testsdgrpMess(self):
        u'验证发送一定数量的群消息'
        self.oneuser.login()
        self.assertTrue(self.oneuser.sendgroupMess(groupmess_num), True)
        self.twouser.quitBrowser()
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
    def testgrpMessNum(self):
        u'验证发送的群消息和数量其他成员是否收到'
        self.twouser.login()
        self.oneuser.login()
        self.oneuser.sendgroupMess(groupmess_num)
        self.assertTrue(self.twouser.groupMessNum(groupmess_num), True)
        self.twouser.quitBrowser()
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
    def testDelMember(self):
        u'验证删除群成员'
        self.oneuser.login()
        global nowuser
        result, nowuser = self.oneuser.operateMember(4)
        self.four = ChatGroup(self.browser, nowuser, gpasswd, url, user1, groupname)
        self.four.login()
        self.assertTrue(self.four.verifyDelete(nowuser), True)
        self.four.applyjoin(groupnum)
        self.twouser.quitBrowser()
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.four.quitBrowser()
    def testAddBlack(self):
        u'验证将成员加入黑名单'
        self.oneuser.login()
        global blackuser
        result, blackuser = self.oneuser.operateMember(3)
        self.assertTrue(self.oneuser.verifyBlkList(blackuser), True)
        self.twouser.quitBrowser()
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
    def testRemoveBlack(self):
        u'验证将黑名单的成员移除'
        self.oneuser.login()
        self.assertTrue(self.oneuser.groupRemoveblack(), True)
        self.twouser.quitBrowser()
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
    def testMute(self):
        u'验证对某群成员禁言'
        self.other = ChatGroup(self.browser, blackuser, gpasswd, url, user1, groupname)
        self.other.login()
        self.other.applyjoin(groupnum)
        self.other.quitBrowser()
        self.oneuser.login()
        a, muteuser = self.oneuser.operateMember(2)
        self.four = ChatGroup(self.driver3, muteuser, gpasswd, url, user1, groupname)
        self.four.login()
        self.four.sendgroupMess(groupmess_num)
        self.assertFalse(self.oneuser.groupMessNum(groupmess_num), False)
        self.oneuser.quitBrowser()
        self.four.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testRemoveMute(self):
        u'验证对禁言的成员解除禁言'
        self.oneuser.login()
        a, muteuser = self.oneuser.operateMember(2)
        self.four = ChatGroup(self.browser, muteuser, gpasswd, url, user1, groupname)
        self.four.login()
        self.four.sendgroupMess(groupmess_num)
        self.assertTrue(self.oneuser.groupMessNum(groupmess_num), True)
        self.oneuser.quitBrowser()
        self.four.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testaddGrpAdmin(self):
        u'验证将成员转为管理员'
        self.oneuser.login()
        a, adminuser = self.oneuser.operateMember(1)
        self.assertTrue(self.oneuser.groupadmin(groupnum,adminuser), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testRemoveAdmin(self):
        u'验证解除管理员权限'
        self.oneuser.login()
        a, adminuser = self.oneuser.operateMember(1)
        self.assertFalse(self.oneuser.groupadmin(groupnum, adminuser), False)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testModifyGrpName(self):
        u'验证修改群名称'
        self.oneuser.login()
        self.assertTrue(self.oneuser.modifyGrpName(), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testcleanGroupMess(self):
        u'验证清除群消息'
        self.oneuser.login()
        self.assertTrue(self.oneuser.cleangrpMessage(groupmess_num),True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testdissolveGroup(self):
        u'验证解散群聊功能'
        self.oneuser.login()
        self.assertTrue(self.oneuser.dissolveGroup(groupnum), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testpublicGrpYES(self):
        u'验证创建需要群主审核的公开'
        self.oneuser.login()
        global PubgroupYES
        result,PubgroupYES = self.oneuser.publicgroupYES()
        self.assertTrue(result, True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testRefusejoinGrp(self):
        u'验证拒绝加入审核的公开群'
        self.oneuser.login()
        self.twouser.login()
        self.twouser.applyPubGrp(PubgroupYES)
        self.oneuser.refusejoinGrp()
        result,gn = self.twouser.verifyjoin()
        self.assertFalse(result,False)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testAgreejoinGrp(self):
        u'验证同意加入审核的公开群'
        self.oneuser.login()
        self.twouser.login()
        self.twouser.applyPubGrp(PubgroupYES)
        self.oneuser.agreejoinGrp()
        self.assertTrue(self.twouser.verifyjoin(), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testGrpYESmessage(self):
        u'验证审核公开群的收发消息功能'
        self.twouser.login()
        self.oneuser.login()
        self.oneuser.sendgroupMess(groupmess_num)
        self.assertTrue(self.twouser.groupMessNum(groupmess_num),True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testGrpYESdissolve(self):
        u'验证解散需要审核的公开群'
        self.oneuser.login()
        self.assertTrue(self.oneuser.dissolveGroup(PubgroupYES), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testprivaGrpAllow(self):
        u'验证创建允许成员邀请私有群'
        self.oneuser.login()
        global privGroupNum
        reault, privGroupNum = self.oneuser.privaGrpAllow()
        self.assertTrue(reault,True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testprivaGrpInvite(self):
        u'验证允许邀请的私有群成员是否可以邀请'
        self.oneuser.login()
        self.oneuser.invitemember(user2)
        self.twouser.login()
        self.twouser.invitemember(user3)
        self.threeuser.login()
        result,gn = self.threeuser.verifyjoin()
        self.assertTrue(result, True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testGrpAllowSendMess(self):
        u'验证允许邀请的私有群发送消息'
        self.twouser.login()
        self.oneuser.login()
        self.oneuser.sendgroupMess(groupmess_num)
        self.assertTrue(self.twouser.groupMessNum(groupmess_num), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testGrpAllowDissovle(self):
        u'验证允许邀请的私有群解散'
        self.oneuser.login()
        self.assertTrue(self.oneuser.dissolveGroup(privGroupNum), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testPrivateGrpNoAllow(self):
        u'验证创建不允许成员邀请的私有群'
        self.oneuser.login()
        global privGroupNumNO
        result,privGroupNumNO = self.oneuser.privaGrpNoAllow()
        self.assertTrue(result, True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testPrivateOwnerInvite(self):
        u'验证不允许成员邀请的私有群群主邀请成功'
        self.oneuser.login()
        self.oneuser.invitemember(user2)
        self.twouser.login()
        result, gn = self.twouser.verifyjoin()
        self.assertTrue(result, True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testPrivateMemberInvite(self):
        u'验证不允许成员邀请的私有群成员邀请失败'
        self.twouser.login()
        self.twouser.invitemember(user3)
        self.threeuser.login()
        result, gn = self.threeuser.verifyjoin()
        self.assertFalse(result, False)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testPrivGrpSendMess(self):
        u'验证不允许成员邀请的群发送消息'
        self.twouser.login()
        self.oneuser.login()
        self.oneuser.sendgroupMess(groupmess_num)
        self.assertTrue(self.twouser.groupMessNum(groupmess_num), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()
    def testPrivGrpNoDissovle(self):
        u'验证不允许成员邀请的群解散'
        self.oneuser.login()
        self.assertTrue(self.oneuser.dissolveGroup(privGroupNumNO), True)
        self.oneuser.quitBrowser()
        self.threeuser.quitBrowser()
        self.twouser.quitBrowser()

    def tearDown(self):
        self.oneuser = None
        self.twouser = None
        self.threeuser = None