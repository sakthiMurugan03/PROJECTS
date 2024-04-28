while(True):
    print("""
                                            ********************************************************************************
             
                                                                   WELCOME TO FAS HOSPITALS PVT. LTD. 

                                            ********************************************************************************
    """)




    
    import mysql.connector
    passwd=str(input("ENTER THE DATABASE PASSWORD: "))

    
    mysql=mysql.connector.connect(host="localhost",user="root",passwd="root")
    mycursor=mysql.cursor()

   
    mycursor.execute("create database if not exists FAShospitals")
    mycursor.execute("use FAShospitals")

   
    mycursor.execute("create table if not exists patientdetails(puid int(10) primary key,name varchar(30) not null,sex varchar(20),age int(3),address varchar(50),contact varchar(10),doctor_recommended varchar(30))")
    mycursor.execute("create table if not exists doctordetails(name varchar(30) primary key,specialisation varchar(40),age int(2),address varchar(30),contact varchar(15),fees int(10),monthly_salary int(10))")
    mycursor.execute("create table if not exists nursedetails(name varchar(30) primary key,age int(2),address varchar(30),contact varchar(15),monthly_salary int(10))")
    mycursor.execute("create table if not exists otherworkersdetails(name varchar(30) primary key,age int(2),address varchar(30),contact varchar(15),monthly_salary int(10))")

    
    mycursor.execute("create table if not exists user_data(username varchar(30) primary key,password varchar(30) default'000')")

    
    while(True):
        print("""
                                                                                1. SIGN IN (LOGIN)

                                                                                2. SIGN UP (REGISTER)
                                                                                """)
    
        r=int(input("Enter your choice: "))
    

    
    
        
        if r==2:
            print("""


                                                    ********************************************************************************
                                                                                PLEASE REGISTER YOURSELF
                                                    ********************************************************************************
                                                    """)
            u=input("ENTER YOUR PREFERRED USERNAME!!:")
            p=input("ENTER YOUR PREFERRED PASSWORD (PASSWORD SHOULD BE STRONG!!!:")


            
            mycursor.execute("insert into user_data values('"+u+"','"+p+"')")
            mysql.commit()
    
    
            print("""
                                                    ********************************************************************************
                                                    !!!!!!!!!!!!!!!!!!!!!!!!!!!REGISTERED SUCCESSFULLY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                                    ********************************************************************************
                                                    """)
            x=input("Enter any key to continue: ")






        
        elif r==1:
        
        

                print("""
                                                        ********************************************************************************
                                                        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!  {{SIGN IN }}  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                                        ********************************************************************************
                                                        """)
                un=input("ENTER THE USERNAME: ")
                ps=input("ENTER THE PASSWORD: ")
                
                mycursor.execute("select password from user_data where username='"+un+"'")
                row=mycursor.fetchall()
                for i in row:

                    
                    a=list(i)
                    if a[0]==str(ps):
                        while(True):
                            
                            print("""
                                                                      1.ADMINISTRATION
                                                                      2.PATIENT (ADMISSION NAD DISCHARGE PROCESS)
                                                                      3.SIGN OUT
                                                                      
                                                                      """)
    

                            
                            a=int(input("ENTER YOUR CHOICE FROM ABOVE OPTIONS: "))
                            
                            if a==1:
                                print("""
                                                                          1. SHOW DETAILS
                                                                          2. ADD NEW MEMBER
                                                                          3. DELETE EXISTING ONE
                                                                          4. EXIT
                                                                          """)
                                b=int(input("ENTER YOUR CHOICE FROM ABOVE OPTIONS: "))
                                
                                if b==1:
                                    print("""
                                                                                1. DOCTOR DETAILS
                                                                                2. NURSE DETAILS
                                                                                3. OTHER WORKERS
                                                                                """)
                                    
                                    
                                    
                                    c=int(input("ENTER YOUR CHOICE FROM ABOVE OPTIONS: "))
                                    
                                    if c==1:
                                        mycursor.execute("select * from doctordetails")
                                        row=mycursor.fetchall()
                                        for i in row:
                                            b=0
                                            v=list(i)
                                            k=["NAME","SPECIALISATION","AGE","ADDRESS","CONTACT","FEES","MONTHLY_SALARY"]
                                            d=dict(zip(k,v))
                                            print(d)
                                        
                                    elif c==2:
                                        mycursor.execute("select * from nursedetails")
                                        row=mycursor.fetchall()
                                        for i in row:
                                            v=list(i)
                                            k=["NAME","SPECIALISATION","AGE","ADDRESS","CONTACT","MONTHLY_SALARY"]
                                            d=dict(zip(k,v))
                                            print(d)
                                    
                                    elif c==3:
                                        mycursor.execute("select * from otherworkersdetails")
                                        row=mycursor.fetchall()
                                        for i in row:
                                            v=list(i)
                                            k=["NAME","SPECIALISATION","AGE","ADDRESS","CONTACT","MONTHLY_SALARY"]
                                            d=dict(zip(k,v))
                                            print(d)
                                
                                elif b==2:
                                    print("""




                                                                                    1. DOCTOR DETAILS
                                                                                    2. NURSE DETAILS
                                                                                    3. OTHER WORKERS
                                                                                    """)
                                    c=int(input("ENTER YOUR CHOICE: "))
                                    
                                    if c==1:
                                      
                                      name=input("ENTER DR.NAME: ")
                                      spe=input("ENTER SPECIALISATION: ")
                                      age=input("ENTER AGE: ")
                                      add=input("ENTER ADDRESS: ")
                                      cont=input("ENTER CONTACT NO.: ")
                                      fees=input("ENTER FEES: ")
                                      ms=input("ENTER MONTHLY_SALARY: ")
                                      
                                      mycursor.execute("insert into doctordetails values('"+name+"','"+spe+"','"+age+"','"+add+"','"+cont+"','"+fees+"','"+ms+"')")
                                      mysql.commit()
                                      print("SUCCESSFULLY ADDED...!")
                                    
                                    elif c==2:
                                      
                                      name=input("ENTER NURSE NAME: ")
                                      age=input("ENTER AGE: ")
                                      add=input("ENTER ADDRESS: ")
                                      cont=input("ENTER CONTACT NO.: ")
                                      ms=int(input("ENTER MONTHLY_SALARY: "))
                                      
                                      mycursor.execute("insert into nursedetails values('"+name+"','"+age+"','"+add+"','"+cont+"','"+str(ms)+"')")
                                      mysql.commit()
                                      print("SUCCESSFULLY ADDED...!")
                                    
                                    elif c==3:
                                  
                                      name=input("ENTER WORKER NAME: ")
                                      age=input("ENTER AGE: ")
                                      add=input("ENTER ADDRESS: ")
                                      cont=input("ENTER CONTACT NO.: ")
                                      ms=input("ENTER MONTHLY_SALARY: ")



                                      
                                      mycursor.execute("insert into otherworkersdetails values('"+name+"','"+age+"','"+add+"','"+cont+"','"+ms+"')")
                                      mysql.commit()
                                      print("SUCCESSFULLY ADDED...!")
                                
                                elif b==3:
                                   print("""
                                                                                    1. DOCTOR DETAILS


                                                                                    2. NURSE DETAILS
                                                                                    3. OTHER WORKERS
                                                                                    """)
                                   c=int(input("ENTER YOUR CHOICE FROM ABOVE OPTIONS: "))
                                   
                                   if c==1:
                                       name=input("ENTER DOCTOR'S NAME: ")
                                       mycursor.execute("select * from doctordetails where name='"+name+"'")
                                       row=mycursor.fetchall()
                                       print(row)
                                       p=input("You really wanna delete this data? (y/n): ")
                                       if p=="y":
                                           mycursor.execute("Delete from doctordetails where name='"+name+"'")
                                           mysql.commit()
                                           print("SUCCESSFULLY DELETED...!")
                                       else:
                                           print("NOT DELETED")
                                       


                                      
                                   
                                   elif c==2:
                                       name=input("ENTER NURSE NAME: ")
                                       mycursor.execute("select * nursedetails where name='"+name+"'")
                                       row=mycursor.fetchall()
                                       print(row)
                                       p=input("You really wanna delete this data? (y/n): ")
                                       if p=="y":
                                           mycursor.execute("Delete from nursedetails where name='"+name+"'")
                                           mysql.commit()
                                           print("SUCCESSFULLY DELETED...!")
                                       else:
                                           print("NOT DELETED")
                                   
                                   elif c==3:
                                       name=input("ENTER THE WORKER NAME: ")
                                       mycursor.execute("select * from workersdetails where name='"+name+"'")
                                       row=mycursor.fetchall()
                                       print(row)
                                       p=input("You really wanna delete this data? (y/n): ")
                                       if p=="y":
                                           mycursor.execute("delete from otherworkersdetails where name='"+name+"'")
                                           mysql.commit()
                                           print("SUCCESSFULLY DELETED...!")
                                       else:
                                           print("NOT DELETED")
                                elif b==4:
                                    break
                               
                            
                            elif a==2:
                                
                                print("""
                                                                          1. SHOW  PATIENT DETAILS
                                                                          2. ADD  NEW PATIENT
                                                                          3. DISCHARGE PATIENT
                                                                          4. EXIT
                                                                          """)
                                b=int(input("ENTER YOUR CHOICE: "))
                                
                                if b==1:
                                    mycursor.execute("select * from patientdetails")
                                    row=mycursor.fetchall()
                                    for i in row:
                                        b=0
                                        v=list(i)
                                        k=["NAME","SEX","AGE","ADDRESS","CONTACT"]
                                        d=dict(zip(k,v))
                                        print(d)
                                    
                                
                                elif b==2:
                                    puid=input("ENTER THE ID OF THE PATIENT")
                                    name=input("ENTER NAME: ")
                                    sex=input("ENTER SEX: ")
                                    age=input("ENTER AGE: ")
                                    address=input("ADDRESS: ")
                                    contact=input("CONTACT NUMBER: ")
                                    recdoc=input("ENTER THE REC DOC")
                                    mycursor.execute ("insert into patientdetails values('"+puid+"','"+name+"','"+sex+"','"+age+"','"+address+"','"+contact+"','"+recdoc+"')")
                                    mysql.commit()
                                    mycursor.execute("select * from patientdetails")
                                    for i in mycursor:
                                        v=list(i)
                                        k=['PID','NAME','SEX','AGE','ADDRESS','CONTACT']
                                        print(dict(zip(k,v)))
                                        print("""
                                                        ********************************************************************************
                                                        !!!!!!!!!!!!!!!!!!!!!!!!!!!REGISTERED SUCCESSFULLY!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                                        ********************************************************************************
                                                        """)
                                
                                elif b==3:
                                    name=input("ENTER THE PATIENT NAME: ")
                                    mycursor.execute("select * from patientdetails where name='"+name+"'")
                                    row=mycursor.fetchall()
                                    print(row)
                                    bill=input("HAS HE PAID ALL THE BILLS ? (y/n):")
                                    if bill=="y":
                                        mycursor.execute("delete from patientdetails where name='"+name+"'")
                                        mysql.commit()
                                        print("Patient Successfully Discharged")
                                
                                elif b==4:
                                    break
                            
                            elif a==3:
                                break
                                    



                                
                  
                    else:
                        break
