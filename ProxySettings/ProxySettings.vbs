Dim proxyEnabled,proxyServer ,proxyOverride

' ���ô����������Ϣ
proxyServer = "127.0.0.1:10809"  ' �����������ַ�Ͷ˿�
proxyServerPhone = "192.168.43.1:2080"

proxyRegPath = "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\"
' ����WScript.Shell����
Set objShell = WScript.CreateObject("WScript.Shell")

On Error Resume Next
proxyEnabled = objShell.RegRead(proxyRegPath & "ProxyEnable")
If Err.Number <> 0 Then
    proxyEnabled = 0 ' Ĭ��Ϊ����
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

' ���ô���
objShell.RegWrite (proxyRegPath & "ProxyEnable"), 1, "REG_DWORD"
' ���ô��������
objShell.RegWrite (proxyRegPath & "ProxyServer"), proxyServerPhone, "REG_SZ"
' ˢ��ϵͳ�������ã�ʹ������Ч
objShell.Run "cmd /c ipconfig /flushdns", 0, True
WScript.Echo "����������" & vbCrLf & "���������: " & ProxyServerPhone
MsgBox "����رմ���"
' ��ԭ����
objShell.RegWrite (proxyRegPath & "ProxyEnable"), proxyEnabled, "REG_DWORD"
objShell.RegWrite (proxyRegPath & "ProxyServer"), proxyServer, "REG_SZ"
objShell.RegWrite (proxyRegPath & "ProxyOverride"), proxyOverride, "REG_SZ"
' ˢ��ϵͳ�������ã�ʹ������Ч
objShell.Run "cmd /c ipconfig /flushdns", 0, True

WScript.Echo "�����ѻ�ԭ" & vbCrLf & "����״̬:" & IE(proxyEnabled) & vbCrLf & "���������: " & proxyServer & vbCrLf & "�ƹ�����:" & proxyOverride

Set objShell = Nothing

Function IE(Enint)
    If Enint=1 Then
        IE = "����"
    Else
        IE = "�ر�"
    End If
End function