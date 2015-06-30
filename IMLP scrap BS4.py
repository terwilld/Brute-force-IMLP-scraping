from bs4 import BeautifulSoup
import requests,time,csv,copy


    #Get page one
r = requests.get('http://www.ironman.com/triathlon/events/americas/ironman/lake-placid/results.aspx#axzz3ZGxvpGki')
raw_html=r.text
    #Soupify
soup = BeautifulSoup(raw_html)
    #Make list of all elements surrounded by td tags.  This is our lowest denominator
results=soup.findAll('td')


counter=1
list_of_people=[]
person=[]
for x in results:
    #print x, 'counter',counter,x.text
    if counter == 1 or counter == 6 or counter == 7 or counter == 8 or counter == 9:
        person+=[x.text]

    counter+=1
    if counter>10:
        counter-=10
        list_of_people+=[person]
        person=[]

for k in range(2,139):      #139= true max possibly make a large max and an except break
    print k,len(list_of_people),'page','len uncleaned_html'
    time.sleep(0.100)
    r = requests.get('http://www.ironman.com/triathlon/events/americas/ironman/lake-placid/results.aspx?p='+str(k)+'#axzz3ZGxvpGki')
        #   Essentially repeat the steps done above for the first page
    raw_html=r.text
        #Soupify
    soup = BeautifulSoup(raw_html)
        #Make list of all elements surrounded by td tags.  This is our lowest denominator
    results=soup.findAll('td')

    counter=1
    person=[]
    for x in results:
        #print x, 'counter',counter,x.text
        if counter == 1 or counter == 6 or counter == 7 or counter == 8 or counter == 9:
            person+=[x.text]

        counter+=1
        if counter>10:
            counter-=10
            list_of_people+=[person]
            person=[]
temp=[]
little_temp=[]

    #convert evertying from unicode
for person in list_of_people:
    for y in person:
        try:
            temp_y=str(y)
        except:
            b=1
        little_temp+=[temp_y]
    temp+=[little_temp]
    little_temp=[]
list_of_people=copy.deepcopy(temp)

    #sep last name and first name into two seperate things
big_temp=[]
for person in list_of_people:
    little_temp=[]
    for i in range(0,len(person)):
        if i ==0:
            my_string=person[i]
            double=[x.strip() for x in my_string.split(',')]
            print double
            little_temp+=double
        else:
            little_temp+=[person[i]]
    big_temp+=[little_temp]
list_of_people=copy.deepcopy(big_temp)
with open('some.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(list_of_people)
