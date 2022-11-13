#mySqlFunction.py
#Use : from mySqlFunction import *
#from util.basic import *
import re
import sqlite3

def isTableExists( dbName ,tableName ):
    con = sqlite3.connect( dbName )
    cur = con.cursor()
    cur.execute('''
      SELECT NAME FROM sqlite_master WHERE TYPE="table"
      AND name="%s";''' % tableName )
    qd = cur.fetchone()
    if qd==None:
        return False
    else:
        return True

def getTableName( dbName , prResult= False ):
    con = sqlite3.connect( dbName )
    cur = con.cursor()
    cur.execute('SELECT NAME FROM sqlite_master WHERE TYPE="table"')
    qd = cur.fetchall()
    tableList = [ tb[0] for tb in qd ]

    if prResult:
        print( '* Table List *' )
        for tb in tableList:
            print( tb)

    return tableList

def getColumnName( dbName ,tableName ,prResult= False ):
    tableList = getTableName( dbName )
    tableList = [ tname.upper() for tname in tableList ]
    if tableName.upper() not in tableList:
        return []
    con = sqlite3.connect( dbName )
    cur = con.cursor()
    cur.execute("SELECT * FROM %s LIMIT 1;" % tableName )
    con.commit()
    cur.close()
    con.close()


    fieldList = [ fd[0] for fd in cur.description ]

    if prResult:
        print( '* Column List *' )
        for fd in fieldList:
            print( fd)

    return fieldList

def getTypeOfColumn(dbName ,tableName ,prResult= False ):
    rtnDict = {}
    con = sqlite3.connect( dbName )
    cur = con.cursor()
    cur.execute( 'PRAGMA table_info(%s)' % tableName )
    qd = cur.fetchall()

    for fd in qd:
        rtnDict[fd[1]] = fd[2]
        if prResult:
            print( fd)

    con.commit()
    cur.close()
    con.close()
    return rtnDict

def getIndexNameList(dbName ,tableName ,prResult= False ):
    con = sqlite3.connect( dbName )
    cur = con.cursor()
    cur.execute( 'PRAGMA INDEX_LIST(%s)' % tableName )
    qd = cur.fetchall()
    # [(0, 'miofcid', 0)]
    # seq Unique numeric ID of index, name ,unique Uniqueness flag (nonzero if UNIQUE index.)
    if prResult:
        print(qd)
    con.commit()
    cur.close()
    con.close()
    del cur
    del con
    return qd

def getTypeOfVaccum(dbName ,prResult= False ):
    #rtnDict['AutoVaccum'] = 'None'
    rtnStr = ''
    con = sqlite3.connect( dbName )
    cur = con.cursor()
    cur.execute( "PRAGMA auto_vacuum;" )
    qd = cur.fetchall()
    for vstate in qd:
        if vstate[0]==0:
            rtnStr = 'NONE'
        elif vstate[0]==1:
            rtnStr = 'FULL'
        elif vstate[0]==2:
            rtnStr = 'INCREMENTAL'
        if prResult:
            print( 'AutoVaccum : %s' % rtnStr )

    con.commit()
    cur.close()
    con.close()
    del cur
    del con
    return rtnStr

def getSqlVersion( prResult= False ):
    con = sqlite3.connect(':memory:')
    cur = con.cursor()
    version = cur.execute( 'SELECT sqlite_version()').fetchone()[0]
    if prResult:
        print( version)
    con.commit()
    cur.close()
    con.close()
    del cur
    del con
    return version

def vacuum_database( dbName ):
   if dbName =="Setting.db":
      db_file  = os.path.join( os.path.abspath("."), "BasicDB", dbName )
   else:
      db_file = dbName

   con = sqlite3.connect( db_file )
   con.isolation_level = None
   con.execute("VACUUM;")
   con.isolation_level = ''
   con.commit()
   con.close()
   del con

def get_query_dict( sql ):
    # 쿼리를 받아서 select  from where groupby orderby limit 로 분리해줌.
    # "SELECT 0, OrderOption, COUNT(*), SUM(OrderCnt) FROM ESOrder  WHERE TransComp=0  GROUP BY OrderOption ORDER BY site"
    sql_dict = {}
    sql = sql.replace("\n"," ")
    sql = sql.replace("\t"," ")

    sql = re.sub(" from ",   " FROM ", sql, flags=re.IGNORECASE)
    sql = re.sub(" where ",  " WHERE ", sql, flags=re.IGNORECASE)
    sql = re.sub(" order by ", " ORDER BY ", sql, flags=re.IGNORECASE)
    sql = re.sub(" group by ", " GROUP BY ", sql, flags=re.IGNORECASE)
    sql = re.sub(" limit ",    " LIMIT ", sql, flags=re.IGNORECASE)

    sql_dict = { 'select':'', 'from':'', 'where':'', 'groupby':'', 'orderby':'', 'limit':'' }

    fromPos    = sql.find(' FROM ')
    wherePos   = sql.find(' WHERE ')
    groupbyPos = sql.find(' GROUP BY ')
    orderbyPos = sql.find(' ORDER BY ')
    limitPos   = sql.find(' LIMIT ')
    selEndPos  = 0
    # get Select
    if fromPos != -1:
        sql_dict['select'] = sql[7:fromPos].strip()
        getPos = fromPos
    elif wherePos != -1:
        sql_dict['select'] = sql[7:wherePos].strip()
        getPos = wherePos
    elif groupbyPos != -1:
        sql_dict['select'] = sql[7:groupbyPos].strip()
        getPos = groupbyPos
    elif orderbyPos != -1:
        sql_dict['select']  = sql[7:orderbyPos].strip()
        getPos = orderbyPos
    elif limitPos != -1:
        sql_dict['select']  = sql[7:limitPos].strip()
        getPos = limitPos
    else:               # from where groupby orderby limit 다없으면 끝
        sql_dict['select']  = sql.strip()
        return sql_dict
    # get from
    if fromPos != -1:
        if wherePos != -1:
            sql_dict['from'] = sql[ getPos+6: wherePos ].strip()
            getPos = wherePos
        elif groupbyPos != -1:
            sql_dict['from'] = sql[getPos+6:groupbyPos].strip()
            getPos = groupbyPos
        elif orderbyPos != -1:
            sql_dict['from']  = sql[getPos+6:orderbyPos].strip()
            getPos = orderbyPos
        elif limitPos != -1:
            sql_dict['from']  = sql[getPos+6:limitPos].strip()
            getPos = limitPos
        else:
            sql_dict['from']   = sql[ getPos+6: ].strip()
            return sql_dict
    else:
        sql_dict['fromPos']   = ''
    # get where
    if wherePos != -1:
        if groupbyPos != -1:
            sql_dict['where']   = sql[ getPos+7: groupbyPos ].strip()
            getPos = groupbyPos
        elif orderbyPos != -1:
            sql_dict['where']   = sql[ getPos+7: orderbyPos ].strip()
            getPos = orderbyPos
        elif limitPos != -1:
            sql_dict['where']   = sql[ getPos+7: limitPos ].strip()
            getPos = limitPos
        else:
            sql_dict['where']   = sql[ getPos+7: ].strip()
            return sql_dict
    # get groupby
    if groupbyPos != -1:
        if orderbyPos != -1:
            sql_dict['groupby'] = sql[ getPos + 10:orderbyPos].strip()
            getPos = orderbyPos
        elif limitPos != -1:
            sql_dict['groupby'] = sql[ getPos + 10:limitPos].strip()
            getPos = limitPos
        else:
            sql_dict['groupby'] = sql[ groupbyPos + 10:].strip()
            return sql_dict
    # get orderby
    if orderbyPos != -1:
        if limitPos != -1:
            sql_dict['orderby'] = sql[ getPos + 10:limitPos].strip()
            getPos = limitPos
        else:
            sql_dict['orderby'] = sql[ orderbyPos + 10:].strip()
            return sql_dict
    # get limit
    if limitPos != -1:
        sql_dict['limit'] = sql[ limitPos + 7:].strip()
        
    return sql_dict


def make_sql_with_dict( sql_dict , subquerys = [] ):
    # dict 의 from where groupby orderby limit 를 합쳐서 쿼리 완성
    # subquery  는 원본 sql 내에 #subquery# 로 지정후 subquery 리스트 전달.
    sql  =  "SELECT " + sql_dict['select']
    if sql_dict['from'] != '':
        sql +=  " FROM " + sql_dict['from']
    if sql_dict['where'] != '':
        sql +=  " WHERE " + sql_dict['where']
    if sql_dict['groupby'] != '':
        sql +=  " GROUP BY " + sql_dict['groupby']
    if sql_dict['orderby'] != '':
        sql +=  " ORDER BY " + sql_dict['orderby']
    if sql_dict['limit'] != '':
        sql +=  " LIMIT " + sql_dict['limit']

    if subquerys:
        for i in range(len(subquerys)):
            sql = sql.replace( "#subquery#", subquerys[i],1)
    return sql


def get_datas_for_page_from_db( db_path, sql, page_info = None, subquerys = [] ):
    # get_query_dict     :  select from where groupby orderby limit
    # make_sql_with_dict
    srcQueryDict = get_query_dict( sql )
    # 총갯수 가져오기
    cntQueryDict = srcQueryDict.copy()
    cntSubquerys = subquerys[:]
    # subquery 가 select 에 있을때는 count 할때 빼야함
    if subquerys:        
        selectSubqueryCnt= cntQueryDict['select'].count("#subquery#")
        cntSubquerys = cntSubquerys[ selectSubqueryCnt: ]    
    cntQueryDict['select'] = "count(*)"
    cntQueryDict['orderby']= ''
        
    con = sqlite3.connect( db_path )
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    dataCnt = cur.execute( make_sql_with_dict(cntQueryDict, cntSubquerys) ).fetchone()[0]
    if page_info is not None:
        srcQueryDict['limit'] = "%s,%s"%\
                ((page_info['page']-1)*page_info['per_page'], page_info['per_page'])
    datas   = cur.execute( make_sql_with_dict(srcQueryDict, subquerys=subquerys) ).fetchall()
    cur.close()
    con.close()
    return dataCnt, datas

