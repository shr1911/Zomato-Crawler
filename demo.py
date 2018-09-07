# encoding: utf-8
import requests
from lxml import html
import csv

def crawl():
    # First page of mumbai-restaurants
    pageLinks = ['https://www.zomato.com/mumbai/restaurants?&page=2']
    #pageLinks=" "
    # Making list of all links of pages under mumbai-restaurants category (temporary)
    for i in range(67,71):
        a = 'https://www.zomato.com/mumbai/restaurants?'+'&page='+str(i)
        pageLinks.append(a)
    getmorelinks(pageLinks)
	

def getmorelinks(pageLinks):
    # Intializing list for storing restaurant link each pages
    restrauLinks = []

    # Fetching links of all restaurants  from each page
    for i in range(0,len(pageLinks)):
        print(pageLinks[i])
        page = requests.get(pageLinks[i],headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"})
        restrau = page.text
        print('abc')

        # Count of total restaurants on given page
        c = restrau.count('<a class="result-title hover_feedback zred bold ln24   fontsize0 " href="')
        print(c)
        n = 0
        
        while(n < c):
            index = restrau.find('<a class="result-title hover_feedback zred bold ln24   fontsize0 " href="')
            # (74 is the count of characters in above find('<a class=......') string)
            index2 = restrau.find('"',index+74)
            link = restrau[index+73:index2]
            print(link)
            restrauLinks.append(link)
            n += 1
            restrau = restrau[index2+1:]
    maincrawl(restrauLinks)

# For some restaurants there are franchise if they have franchise then we need to get links of those franchise also
def getFranchiseLink(restrauLinks):

    franchiseLink = []
    for i in range(0, len(restrauLinks)):
        page = requests.get(restrauLinks[i], headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"})
        franchise = page.text

        # If there is "See 1 more location" near address i.e. it is franchise ---- so if we found that count will be more then 0
        c = franchise.count('<a class="zred fontsize5" href="')
        print(c)
        n = 0

        while (n < c):
            index = franchise.find('<a class="zred fontsize5" href="')
            index2 = franchise.find('"', index + 33)
            link = franchise[index + 32:index2]
            print(link) #page that contains li
            franchiseLink.append(link)
            n += 1
            franchise = franchise[index2 + 1:]


    # From above franchiseLink[] we get link of page that has list of all franchises but from page we now want link of all those franchises in that list
    # but from this list we don't want first link because that is already included in "restrauLink" part i.e. in above getmorelinks() function.
    moreFranchiseLink = []
    for j in range(0, len(franchiseLink)):
        print("Inside more branch function")
        page = requests.get(franchiseLink[j], headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"})
        moreFranchise = page.text
        c = moreFranchise.count('<a class="result-title hover_feedback zred bold ln24   fontsize0 " href="')
        print(c)
        n = 0

        while (n < c):
            index = moreFranchise.find('<a class="result-title hover_feedback zred bold ln24   fontsize0 " href="')
            index2 = moreFranchise.find('"', index + 74)
            link = moreFranchise[index + 73:index2]
            print(link)

            # Do not include first link
            if(n != 0):
                moreFranchiseLink.append(link)
            n += 1
            moreFranchise = moreFranchise[index2 + 1:]
    return moreFranchiseLink
	

def maincrawl(restrauLinks):
    idcount = 1;
    franchiseLink = getFranchiseLink(restrauLinks)
    #print(franchiseLink)

    # Appending franchiseLink with restrauLinks len(franchiseLink)
    for k in range(0, 10):
        restrauLinks.append(franchiseLink[k])

    
    restaurants_dir = "restaurant.csv"
    csv = open(restaurants_dir, "a")
    #columnTitleRow = "placeID, latitude, longitude, name, address, area, city, averageCost, rating, homeDelievery, smokingArea, alcohol, wifi, valetParking, roofTop  \n"
    #csv.write(columnTitleRow)
    excelRow = ""

    restrau_payment_dir = "payment_restrau.csv" 
    payment_csv = open(restrau_payment_dir, "a")
    #columnTitleRow = "placeID, paymentMethod \n"
    #payment_csv.write(columnTitleRow)
    payment_excelRow = ""

    restrau_number_dir = "number_restrau.csv" 
    number_csv = open(restrau_number_dir, "a")
    #columnTitleRow = "placeID, phone \n"
    #number_csv.write(columnTitleRow)
    number_excelRow = ""

    restrau_timing_dir = "timing_restrau.csv" 
    timing_csv = open(restrau_timing_dir, "a")
    #columnTitleRow = "placeID, day, timing \n"
    #timing_csv.write(columnTitleRow)
    timing_excelRow = ""

    restrau_cuisines_dir = "cuisines_restrau.csv" 
    cuisines_csv = open(restrau_cuisines_dir, "a")
    #columnTitleRow = "placeID, cuisines \n"
    #cuisines_csv.write(columnTitleRow)
    cuisines_excelRow = ""

    restrau_reviews_dir = "reviews_restrau.csv" 
    reviews_csv = open(restrau_reviews_dir, "a")
    #columnTitleRow = "placeID, reviews \n"
    #reviews_csv.write(columnTitleRow)
    reviews_excelRow = ""


    for i in range(0,len(restrauLinks)):
    #for i in range(0,3):
        page = requests.get(restrauLinks[i],headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36"})
        pageText = page.text
        tree = html.fromstring(page.text)

        name = ""
        # Name of restaurants
        name = tree.xpath('//h1[@class="res-name left mb0"]/a/text()')
        #[@style="font-size: 100%"]

        
        #Restaurant ID
        restrau_id = '#'+str(idcount)
        idcount += 1
		
        address = ""
        # Address
        add1 = tree.xpath('//div[@class="borderless res-main-address"]/div/span/text()')
        add2 = tree.xpath('//div[@class="borderless res-main-address"]/div/span/span/text()')
        #print(add1)
        #print(add2)
		
        # get reviews
        reviews = tree.xpath('//div[@class="rev-text mbot0 "]/div/@title')
        #print(reviews)
        
        area = ""
		#area
        if(restrau_id != '#13' and restrau_id != '#15'):
            area = add2[0].strip()
        
        city = ""
        #city
        if(len(add1) == 2):
            if(restrau_id != '#1009' and restrau_id != '#93'):
                 city = add1[1].strip().split(",")[1]

        latitude = ""
        longitude = ""
        coordinates = ""
        #coordinates
        c = pageText.count('<div data-is-zomato="true" data-url="https://www.zomato.com/php/staticmap?center=')
        n = 0 
        while(n < c):
            index = pageText.find('<div data-is-zomato="true" data-url="https://www.zomato.com/php/staticmap?center=')
            index2 = pageText.find('&',index+82)
            coordinates = pageText[index+81:index2]
            n += 1
        latitude = coordinates.split(",")[0]
        c = pageText.count('<div class="resmap-text-container">')
        if(c != 0):
             longitude = coordinates.split(",")[1]
		
        average_cost = ""
        # average cost
        # encoding: utf-8
        c = pageText.count('<span tabindex="0" aria-label=" ')
        n = 0 
        while(n < c):
            index = pageText.find('<span tabindex="0" aria-label=" ')
            index2 = pageText.find(' ',index+34)
            average_cost = pageText[index+33:index2]
            n += 1
        
        rating = ""
        # rating
        c = pageText.count('<span class="ratingtext hidden" data-original="Rating: ')
        n = 0 
        while(n < c):
            index = pageText.find('<span class="ratingtext hidden" data-original="Rating: ')
            index2 = pageText.find('/',index+56)
            rating = pageText[index+55:index2]
            n += 1
		
        #payment methods
        payment=tree.xpath('//div[@class="res-info-cft-text fontsize5"]/span/text()')

        # Hours - timing of Restaurants
        timing=tree.xpath('//div[@class="res-week-timetable ui popup bottom left transition hidden"]/table/tr/td/text()')
        print(timing)
		
		# Phone number
        number=tree.xpath('//span[@class="tel"]/text()')
        if(',' in number):
            number.remove(',')

        # get list of cuisines
        cuisines=tree.xpath('//div[@class="res-info-cuisines clearfix"]/a/text()')

        # Print print(restrau_id)
        print(restrau_id)
        
        # Print name of Restaurants
        indexval = 0
        rname = ""
        for i in range(len(name)):
            rname = rname + name[indexval].strip()
            print("Name: " + name[indexval].strip())
            indexval += 1

        # Print address of Restaurants
        address = ""
        indexval = 0
        for i in range(len(add1)+1):
            if(i == (len(add1)-1)):
               if(restrau_id != '#15' and restrau_id != '#882'):
                    address = address + add2[0].strip()
            else: 
               if(restrau_id != '#775' and restrau_id != '#837' and restrau_id != '#773'and restrau_id != '#830'):
                     address = address + add1[indexval].strip()
                     indexval += 1
        print('Address: ', address)

        # Print area
        #print(area)
		
        # Print city
        #print(city)

        # Print coordinates (x, y)
        print(coordinates)
        
        # Print average cost
        print(average_cost) 
        
        # Print Rating
        print(rating)		

        # Print home delivery
        c = pageText.count('<div tabindex="0" aria-labelledby="labelledby_delivery" class="clearfix mb5">')
        if(c == 1):
            home_delivery = 'yes'
            print(home_delivery)
        else:
            home_delivery = 'no' 

        # Print smoking area
        c = pageText.count('<div tabindex="0" aria-label="Smoking Area" class="res-info-feature clearfix mb5">')
        if(c == 1):
            smoking_area = 'yes'
            print(smoking_area)
        else:
            smoking_area = 'no'

        # Alcohol available
        c = pageText.count('<div tabindex="0" aria-labelledby="labelledby_fullbar" class="clearfix mb5">')
        if(c == 1):
            alcohol = 'yes'
            print(alcohol)
        else:
            alcohol = 'no'

        # wifi service
        c = pageText.count('<div tabindex="0" aria-label="Wifi" class="res-info-feature clearfix mb5">')
        if(c == 1):
            wifi = 'yes'
            print(wifi)
        else:
            wifi = 'no'

        # valet parking
        c = pageText.count('<div tabindex="0" aria-label="Valet Parking Available" class="res-info-feature clearfix mb5">')
        if(c == 1):
            valetParking = 'yes'
            print(valetParking)
        else:
            valetParking = 'no'

        # roof top
        c = pageText.count('<div tabindex="0" aria-label="Rooftop" class="res-info-feature clearfix mb5">')
        if(c == 1):
            roofTop = 'yes'
            print(roofTop)
        else:
            roofTop = 'no'

        # Print Payment Methods
        for j in range(0,len(payment)):
            payment[j] = payment[j].strip()
            payment_excelRow = restrau_id +","+ payment[j] + '\n'
            payment_csv.write(payment_excelRow)
        #print('payment: ', payment)

        # Print reviews
        finalReviews = ""
        for j in range(0,len(reviews)):
            #finalReviews[j] = reviews[j].strip()
            reviews_excelRow = restrau_id +',"'+ reviews[j].strip() + '" \n'
            reviews_csv.write(reviews_excelRow)
        #print('reviews: ', reviews)

        # Print timings of Restaturants
        temp = 0
        while(temp < len(timing)):
            timing_excelRow = restrau_id +","+ timing[temp].strip() +","+ timing[temp+1].strip() + '\n'
            timing_csv.write(timing_excelRow)
            temp = temp+2;
        #print('Timings: ', timing)

        # print cusines
        for j in range(0,len(cuisines)):
            cuisines[j] = cuisines[j].strip()
            cuisines_excelRow = restrau_id +","+ cuisines[j] + '\n'
            cuisines_csv.write(cuisines_excelRow)
        #print('cuisines: ', cuisines)

        # Print phone number of Restaurants
        for j in range(0,len(number)):
            number[j] = number[j].strip()
            number_excelRow = restrau_id +","+ number[j] + '\n'
            number_csv.write(number_excelRow)
        #print('Number: ', number)
        print("\n\n")
		
        
        

        excelRow = restrau_id +','+ latitude +','+ longitude +',"'+ rname +'","'+ address +'","'+ area +'","'+ city +'","'+ average_cost +'",'+ rating +','+ home_delivery +','+smoking_area +','+alcohol +','+ wifi +','+ valetParking +','+ roofTop +'\n'
        #print(excelRow)


        csv.write(excelRow)

    csv.close()
		

crawl()