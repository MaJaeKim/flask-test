def format_datetime_han( value, fmt='%y년 %m월 %d일 %H:%M:%S' ):
    # 인풋 string을 유니코드 인코딩 후 디코딩
    uniEncDec =  fmt.encode('unicode-escape').decode()
    # 아웃풋 string 을 인코딩 후 유니코드 디코딩
    uniDec = value.strftime( uniEncDec ).encode().decode('unicode-escape')  
    return uniDec

def format_datetime( value, fmt='%y-%m-%d %H:%M:%S' ):
    return value.strftime( fmt )

def format_datetime_to_sec( value):
    return value[:19]
