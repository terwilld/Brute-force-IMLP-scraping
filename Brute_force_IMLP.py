from bs4 import BeautifulSoup
import csv,requests,time,datetime,urllib,copy
#   To Do
#   Add patriot data
#   make all last names lower case, remove leading space.  format correctly create dictionary for referenceing
#   Add good comments, make clean
#
def extract_athlete_data(athlete_data):
    # removes stuff leading up to last name
    href_index=athlete_data.index('class="athlete">')
    athlete_data=athlete_data[(href_index+len('class="athlete">')):]
    
    #last name llocated from [0] to ,
    comma_index = athlete_data.index(',')
    last_name=str(athlete_data[:comma_index])
    athlete_data=athlete_data[comma_index+1:]                       #gets rid of last name

    # first name from [0] to </a>
    post_index = athlete_data.index('</a>')
    first_name = athlete_data[:post_index]    
    span_index=athlete_data.index('</span>')
    athlete_data=athlete_data[((span_index)+len('</span>')):]      #gets rid of first name

    #remove multiple <td>s
    for i in range(0,4):
        end_td_index=athlete_data.index('</td>')
        athlete_data=athlete_data[(end_td_index+len('</td>')):]


    #extract swim time
    start_td = athlete_data.index('<td>')
    end_td = athlete_data.index('</td>')
    swim_time=athlete_data[(start_td+len('<td>')):end_td]           #remove swim time

    #remove swimtime same as removed other tdx
    for i in range(0,1):
        end_td_index=athlete_data.index('</td>')
        athlete_data=athlete_data[(end_td_index+len('</td>')):]

    #extract bike time
    start_td = athlete_data.index('<td>')
    end_td = athlete_data.index('</td>')
    bike_time=athlete_data[(start_td+len('<td>')):end_td]

    #remove bike time
    for i in range(0,1):
        end_td_index=athlete_data.index('</td>')
        athlete_data=athlete_data[(end_td_index+len('</td>')):]

    #extract run time
    start_td = athlete_data.index('<td>')
    end_td = athlete_data.index('</td>')
    run_time = athlete_data[(start_td+len('<td>')):end_td]
    #print run_time

    #str req for unicode removal... don't understand
    return [str(last_name),str(first_name),str(swim_time),str(bike_time),str(run_time)]


   







#   Page one of IMLP 2014 the URL is different for the first page so done seperately
r = requests.get('http://www.ironman.com/triathlon/events/americas/ironman/lake-placid/results.aspx#axzz3ZGxvpGki')

#only look at the tables with my data
first_index=r.text.index('<tbody>')                 
second_index=r.text.index('</tbody>')
current_results_table=r.text[first_index:second_index]

#divide this data up into a chunk for each athelte
#there are 20 atheltes per page, separated by <tr> and </tr>
un_cleaned_athlete_html=[]

# each athlete gets an index in un_cleaned_athlete_html
# the for loop below adds, cleaning takes place later
# try added incase some pages have less than 20 (namely end of data sets)
# x=2 simply because try statements need an except (I believe)
for i in range(0,20):
    try:
        first_tr_index=current_results_table.index('<tr>')
        second_tr_index=current_results_table.index('</tr>')
        un_cleaned_athlete_html+=[current_results_table[first_tr_index:(second_tr_index+len('</tr>'))]]
        #once athelte data added, remove from raw html
        current_results_table=current_results_table[(second_tr_index+len('</tr>')):]
    except:
        x=2


#   All Remaining pages for IMLP 2014 results
#   Pages 2-139
for k in range(2,139):      #139= true max possibly make a large max and an except break
    print k,len(un_cleaned_athlete_html),'page','len uncleaned_html'
    time.sleep(1.000)
    r = requests.get('http://www.ironman.com/triathlon/events/americas/ironman/lake-placid/results.aspx?p='+str(k)+'#axzz3ZGxvpGki')
    #   Essentially repeat the steps done above for the first page
    first_index=r.text.index('<tbody>')                 
    second_index=r.text.index('</tbody>')
    current_results_table=r.text[first_index:second_index]
    

    for i in range(0,20):
        try:
            first_tr_index=current_results_table.index('<tr>')
            second_tr_index=current_results_table.index('</tr>')
            un_cleaned_athlete_html+=[current_results_table[first_tr_index:(second_tr_index+len('</tr>'))]]
            #once athelte data added, remove from raw html
            current_results_table=current_results_table[(second_tr_index+len('</tr>')):]
        except:
            x=2




    #   I don't understand unicode vs string differences, convert all html parses to string
    #   German character umlat goes fucking ham
temp=[]
for i in range(0,len(un_cleaned_athlete_html)):
    try:    
        temp+=[str(un_cleaned_athlete_html[i])]
    except:
        print i

un_cleaned_athlete_html=copy.deepcopy(temp)

x=extract_athlete_data(un_cleaned_athlete_html[0])
cleaned_athlete_data=[]


    #Clean the data  [last_name, first_name, swim, bike, run]
for x in un_cleaned_athlete_html:
    cleaned_athlete_data+=[extract_athlete_data(x)]


    #Remove the leading space for first names
for i in range(0,len(cleaned_athlete_data)):
    temp = cleaned_athlete_data[i][1]
    if temp[0]==' ':
        temp=temp[1:]
        cleaned_athlete_data[i][1] = copy.deepcopy(temp)
    # Make all names lowercase
    #last name is [0] first name is [1]
    cleaned_athlete_data[i][0]=cleaned_athlete_data[i][0].lower()
    cleaned_athlete_data[i][1]=cleaned_athlete_data[i][1].lower()

#   Process the uncleaned_athlete_html to athlete data
#   function converts mess to [last_name,first_name,swim,bike,run]




with open('some.csv', 'wb') as f:
    writer = csv.writer(f)
    writer.writerows(cleaned_athlete_data)
