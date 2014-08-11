#!/usr/bin/python
# -*- coding: utf-8 -*-
from Yowsup.connectionmanager import YowsupConnectionManager
from config import *
from time import sleep

creator = ""
my_number = "number_to_add"

def waOnAuthSuccess(username):
	print("Logged in with %s" % username)
	methodsInterface.call("ready")

def waOnAuthFailed(username, reason):
	print("Logging failed because %s" % reason)


def onMessageSent(jid, messageId):
	print("Message was sent successfully to %s" % jid)
	methodsInterface.call("message_ack", (jid, messageId))

def onMessageDelivered(jid, messageId):
	print("Message was delivered successfully to %s" % jid)
	methodsInterface.call("delivered_ack", (jid, messageId))

def waOnGroupCreateSuccess(groupJid):
	global wa_group
	wa_group = groupJid
	print('group created! !!!!!! JID: %s !!!' % groupJid)
	methodsInterface.call("message_send", ("%s@s.whatsapp.net" % my_number, "Grupo foi criado com sucesso!")) 

def waOnGroupCreateFail(errorCode):
	print("group creation failed: %s" % errorCode)

def waOnAddParticipantToGroup(jid, group):
	methodsInterface.call("group_addParticipants", (group, (jid,)))
	sleep(1)
	methodsInterface.call("message_send", (jid, "%s Voce foi adicionado ao grupo %s" % (jid, group)))

def waOnAddParticipantsSuccess(jid, groupJid):
	print("%s was add successfully to %s" % (jid, groupJid))

def waOnGroupError(errorCode):
	print("group error %s" % errorCode)

def waOnGroupInfo(jid, owner, subject, subjectOwner, subjectTimestamp, creationTimestamp):
	print('group estou aqui')
	print('%s %s %s %s %s %s' % (jid, owner, subject, subjectOwner, str(subjectTimestamp), str(creationTimestamp)))

def waOnMessageReceived(messageId, jid, messageContent, timestamp, wantsReceipt, pushName, isBroadCast):
	print('group estou no message reived')
	methodsInterface.call("message_ack", (jid, messageId))

def waOnGroupMessageReceived(messageId, jid, author, messageContent, timestamp, wantsReceipt, pushName):
	print('group estou no group message received')
	methodsInterface.call("message_ack", (jid, messageId))

def waNotificationGroupParticipantAdded(groupJid, jid, author, timestamp, messageId, receiptRequested):
	print('group estou no group added participation')
	methodsInterface.call("notification_ack", (groupJid, messageId))

def waNotificationGroupParticipantRemoved(groupJid, jid, author, timestamp, messageId, receiptRequested):
	print('group estou no group removed participation')
	methodsInterface.call("notification_ack", (groupJid, messageId))

ycm = YowsupConnectionManager()
ycm.setAutoPong(True)
signalsInterface = ycm.getSignalsInterface()
methodsInterface = ycm.getMethodsInterface()
signalsInterface.registerListener("auth_fail", waOnAuthFailed)
signalsInterface.registerListener("auth_success", waOnAuthSuccess)
signalsInterface.registerListener("message_received", waOnMessageReceived)
signalsInterface.registerListener("group_messageReceived", waOnGroupMessageReceived)
signalsInterface.registerListener("group_createSuccess", waOnGroupCreateSuccess)
signalsInterface.registerListener("group_createFail", waOnGroupCreateFail)
signalsInterface.registerListener("group_infoError", waOnGroupError)
signalsInterface.registerListener("group_gotInfo", waOnGroupInfo)
signalsInterface.registerListener("notification_groupParticipantAdded", waNotificationGroupParticipantAdded)
signalsInterface.registerListener("notification_groupParticipantRemoved", waNotificationGroupParticipantRemoved)
signalsInterface.registerListener("receipt_messageSent", onMessageSent)
signalsInterface.registerListener("receipt_messageDelivered", onMessageDelivered)
signalsInterface.registerListener("group_addParticipantsSuccess",waOnAddParticipantsSuccess)
methodsInterface.call("auth_login", (username, password))
sleep(1)
methodsInterface.call("group_create", (wa_group,))
sleep(1)
waOnAddParticipantToGroup("%s@s.whatsapp.net" % my_number, wa_group)
