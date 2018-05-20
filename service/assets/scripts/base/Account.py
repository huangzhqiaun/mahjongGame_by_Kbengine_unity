# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
import Functor

class Account(KBEngine.Proxy):
	def __init__(self):
		KBEngine.Proxy.__init__(self)
	
	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
		
	def onClientEnabled(self):
		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("account[%i] entities enable. entityCall:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()

	def reqCreateAvatar(self,name):
		#客户端请求创建一个角色
		#0：表示请求成功
		#1：已经有相同名字的玩家
		#2：创建失败！已经有一个角色了
		if self.isNewPlayer == 0:
			self.client.OnReqCreateAvatar(2)
			return
		
		porps={
			"playerName":name,
		}
		nameEntity = KBEngine.createEntityLocally("CheckName",porps)
		if nameEntity:
			nameEntity.writeToDB(Functor.Functor(self._OnNameSave,name))

	def _OnNameSave(self,name,success,avatar):
		if self.isDestroyed:
			if avatar:
				avatar.destroy()
			return
		if success:
			self.isNewPlayer = 0
			self.playerName_base = name;
			self.playerID_base = self.databaseID+10000
			self.cellData["playerName"] = name
			self.cellData["playerID"] = self.playerID_base
			if self.client:
				self.client.OnReqCreateAvatar(0)
		else:
			self.client.OnReqCreateAvatar(1)

	def onLeaveRoom(self):
		self.destroyCellEntity()