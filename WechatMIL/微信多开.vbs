Dim num,inputvalid

inputvalid=False
Do While Not inputvalid
    num=InputBox("��������","΢�Ŷ࿪","2")

    If num = "" Then
        MsgBox "������ȡ��", vbInformation, "��ʾ"
        WScript.Quit ' �˳��ű�
    End If
    If IsNumeric(num) Then
        num = CInt(num) ' ת��Ϊ����
        If num > 0 Then
            inputValid = True ' ������Ч���˳�ѭ��
        Else
            MsgBox "���������0�����֣�", vbExclamation, "�������"
        End If
    Else
        MsgBox "������Ч�����������֣�", vbExclamation, "�������"
    End If
Loop

Dim objWshShell,wechatPath,objFSO,pathsToCheck,path,i

' �����ļ�ϵͳ�������ڼ���ļ��Ƿ���ڣ�
Set objFSO = CreateObject("Scripting.FileSystemObject")
' ���� WScript.Shell �������ڲ���ע���
Set objWshShell = CreateObject("WScript.Shell")

' ������Ҫ����ע���·���б�����HKLM��HKCU�µĿ���λ�ã�
pathsToCheck = Array( _
    "HKLM\SOFTWARE\Tencent\WeChat\InstallPath", _
    "HKLM\SOFTWARE\Wow6432Node\Tencent\WeChat\InstallPath", _
    "HKCU\SOFTWARE\Tencent\WeChat\InstallPath", _
    "HKCU\SOFTWARE\Tencent\Weixin\InstallPath"_
)

' ���峣����Ĭ�ϰ�װ·������Ϊע������ʧ�ܵĲ��䣩
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
    ' ��ȡע���ֵ
    tempPath = objWshShell.RegRead(path)
    On Error Goto 0
    ' MsgBox tempPath
    ' ��֤·���Ƿ���Ч���Ƿ����WeChat.exe��
    If tempPath <> "" Then
        ' ������ܲ���exe�����
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

'���ע�����δ�ҵ������Ĭ�ϰ�װ·��
If wechatPath = "" Then
    For Each path In defaultPaths
        If objFSO.FileExists(path) Then
            wechatPath = path
            Exit For
        End If
    Next
End If

' �࿪
If wechatPath <> "" Then
    ' MsgBox "�ҵ�΢��·����" & vbCrLf & wechatPath, vbInformation, "���ҳɹ�"
    
    ' ѭ����ָ��������΢��
    For i = 1 To num
        objWshShell.Run """" & wechatPath & """", 1, False
        WScript.Sleep 50 ' ���1�룬�����ͻ
    Next
    
    MsgBox "��Ϊ��� " & num & " ��΢�Ŵ���", vbInformation, "�������"
Else
    MsgBox "δ�ҵ�΢��·����" & vbCrLf & "���ֶ�ָ��΢�Ű�װλ�á�", vbExclamation, "����ʧ��"
End If


MsgBox "���㿪��"&num&"��΢�ţ������˰ɣ�"

' �ͷŶ���
Set objWshShell = Nothing
Set objFSO = Nothing
