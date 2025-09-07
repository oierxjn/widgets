Dim num,inputvalid

inputvalid=False
Do While Not inputvalid
    num=InputBox("开几个？","微信多开","2")

    If num = "" Then
        MsgBox "操作已取消", vbInformation, "提示"
        WScript.Quit ' 退出脚本
    End If
    If IsNumeric(num) Then
        num = CInt(num) ' 转换为整数
        If num > 0 Then
            inputValid = True ' 输入有效，退出循环
        Else
            MsgBox "请输入大于0的数字！", vbExclamation, "输入错误"
        End If
    Else
        MsgBox "输入无效，请输入数字！", vbExclamation, "输入错误"
    End If
Loop

Dim objWshShell,wechatPath,objFSO,pathsToCheck,path,i

' 创建文件系统对象（用于检查文件是否存在）
Set objFSO = CreateObject("Scripting.FileSystemObject")
' 创建 WScript.Shell 对象用于操作注册表
Set objWshShell = CreateObject("WScript.Shell")

' 定义需要检查的注册表路径列表（包含HKLM和HKCU下的可能位置）
pathsToCheck = Array( _
    "HKLM\SOFTWARE\Tencent\WeChat\InstallPath", _
    "HKLM\SOFTWARE\Wow6432Node\Tencent\WeChat\InstallPath", _
    "HKCU\SOFTWARE\Tencent\WeChat\InstallPath", _
    "HKCU\SOFTWARE\Tencent\Weixin\InstallPath"_
)

' 定义常见的默认安装路径（作为注册表查找失败的补充）
defaultPaths = Array( _
    "C:\Program Files\Tencent\WeChat\WeChat.exe", _
    "C:\Program Files (x86)\Tencent\WeChat\WeChat.exe", _
    "D:\Program Files\Tencent\WeChat\WeChat.exe", _
    "D:\Program Files (x86)\Tencent\WeChat\WeChat.exe", _
    "C:\Program Files\Tencent\WeChat\Weixin.exe", _
    "C:\Program Files (x86)\Tencent\WeChat\Weixin.exe", _
    "D:\Program Files\Tencent\WeChat\Weixin.exe", _
    "D:\Program Files (x86)\Tencent\WeChat\Weixin.exe" _
)

wechatPath = ""

For Each path In pathsToCheck
    Dim tempPath

    On Error Resume Next
    ' 读取注册表值
    tempPath = objWshShell.RegRead(path)
    On Error Goto 0
    ' MsgBox tempPath
    ' 验证路径是否有效（是否存在WeChat.exe）
    If tempPath <> "" Then
        ' 处理可能不带exe的情况
        If Right(tempPath, 1) = "\" Then
            fullPath = tempPath & "WeChat.exe"
            If objFSO.FileExists(fullPath) Then
                wechatPath = fullPath
                Exit For
            End if
            fullPath = tempPath & "Weixin.exe"
            If objFSO.FileExists(fullPath) Then
                wechatPath = fullPath
                Exit For
            End if
        Else
            fullPath = tempPath & "\Weixin.exe"
            If objFSO.FileExists(fullPath) Then
                wechatPath = fullPath
                Exit For
            End if
            fullPath = tempPath & "\Weixin.exe"
            If objFSO.FileExists(fullPath) Then
                wechatPath = fullPath
                Exit For
            End if
        End If
    End If
Next

'如果注册表中未找到，检查默认安装路径
If wechatPath = "" Then
    For Each path In defaultPaths
        If objFSO.FileExists(path) Then
            wechatPath = path
            Exit For
        End If
    Next
End If

' 多开
If wechatPath <> "" Then
    ' MsgBox "找到微信路径：" & vbCrLf & wechatPath, vbInformation, "查找成功"
    
    ' 循环打开指定数量的微信
    For i = 1 To num
        objWshShell.Run """" & wechatPath & """", 1, False
        WScript.Sleep 50 ' 间隔1秒，避免冲突
    Next
    
    MsgBox "已为你打开 " & num & " 个微信窗口", vbInformation, "操作完成"
Else
    MsgBox "未找到微信路径！" & vbCrLf & "请手动指定微信安装位置。", vbExclamation, "查找失败"
End If


MsgBox "给你开了"&num&"个微信，满意了吧？"

' 释放对象
Set objWshShell = Nothing
Set objFSO = Nothing
