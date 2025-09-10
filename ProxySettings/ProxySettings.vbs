Dim proxyEnabled,proxyServer ,proxyOverride

' 配置代理服务器信息
proxyServer = "127.0.0.1:10809"  ' 代理服务器地址和端口
proxyServerPhone = "192.168.43.1:2080"

proxyRegPath = "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\"
' 创建WScript.Shell对象
Set objShell = WScript.CreateObject("WScript.Shell")

On Error Resume Next
proxyEnabled = objShell.RegRead(proxyRegPath & "ProxyEnable")
If Err.Number <> 0 Then
    proxyEnabled = 0 ' 默认为禁用
    Err.Clear
End If

proxyServer = objShell.RegRead(proxyRegPath & "ProxyServer")
If Err.Number <> 0 Then
    proxyServer = ""
    Err.Clear
End If

proxyOverride = objShell.RegRead(proxyRegPath & "ProxyOverride")
If Err.Number <> 0 Then
    proxyOverride = ""
    Err.Clear
End If
On Error Goto 0

' 启用代理
objShell.RegWrite (proxyRegPath & "ProxyEnable"), 1, "REG_DWORD"
' 设置代理服务器
objShell.RegWrite (proxyRegPath & "ProxyServer"), proxyServerPhone, "REG_SZ"
' 刷新系统代理设置，使更改生效
objShell.Run "cmd /c ipconfig /flushdns", 0, True
WScript.Echo "代理已启用" & vbCrLf & "代理服务器: " & ProxyServerPhone
MsgBox "点击关闭代理"
' 还原代理
objShell.RegWrite (proxyRegPath & "ProxyEnable"), proxyEnabled, "REG_DWORD"
objShell.RegWrite (proxyRegPath & "ProxyServer"), proxyServer, "REG_SZ"
objShell.RegWrite (proxyRegPath & "ProxyOverride"), proxyOverride, "REG_SZ"
' 刷新系统代理设置，使更改生效
objShell.Run "cmd /c ipconfig /flushdns", 0, True

WScript.Echo "代理已还原" & vbCrLf & "代理状态:" & IE(proxyEnabled) & vbCrLf & "代理服务器: " & proxyServer & vbCrLf & "绕过代理:" & proxyOverride

Set objShell = Nothing

Function IE(Enint)
    If Enint=1 Then
        IE = "开启"
    Else
        IE = "关闭"
    End If
End function