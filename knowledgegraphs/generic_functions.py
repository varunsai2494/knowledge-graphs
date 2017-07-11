

def doubleMatch(string, substringarray):
    match=[item for item in substringarray if  str(" "+str(item).lower().strip()+" ") in str(" "+str(string).lower().strip()+" ")]
    return match


