import csv
import sys
import requests
import json
from collections import Counter
import re

def result(pincode):
    print "Pincode for the location specified is " + pincode

def autocorrect(input_word):
    def words(text): return re.findall(r'\w+', text.lower())

    WORDS = Counter(words(open('autocorrect.txt').read()))

    def P(word, N=sum(WORDS.values())):
        return WORDS[word] / N

    def correction(word):
        return max(candidates(word), key=P)

    def candidates(word):
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

    def known(words):
        return set(w for w in words if w in WORDS)

    def edits1(word):
        letters = 'abcdefghijklmnopqrstuvwxyz'
        splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
        deletes = [L + R[1:] for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R) > 1]
        replaces = [L + c + R[1:] for L, R in splits if R for c in letters]
        inserts = [L + c + R for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

    def edits2(word):
        return (e2 for e1 in edits1(word) for e2 in edits1(e1))

    return correction(input_word)




def callwithAPI(user_input):
    query = ""
    if len(user_input) == 1:
        query = user_input[0]
    else:
        query = user_input[0]
        for x in user_input[1:]:
            query = query + '+' + x
    response = requests.get("http://www.getpincode.info/api/pincode?q=" + query)
    returned_data = response.text
    result = json.loads(returned_data)
    for key in result:
        if key == 'error':
            print "not a valid location"
            exit(0)
    print "PinCode of this location is " + result["pincode"]
def printinfo(Officename,Sub_distname,Districtname,Statename):
    print "Officename - " + Officename
    print "Sub_distname - " + Sub_distname
    print "Districtname - " + Districtname
    print "Statename - " + Statename


def main():
    # declaring variable and converting user input to a list
    reader = csv.DictReader(open('Main.csv'))
    user_inputraw = raw_input("Enter the location of which you want the Pin Code")
    user_inputraw = user_inputraw.split()
    length = len(user_inputraw)
    user_input = []
    if length > 8:
        sys.exit('Enter a short query')
    for keyword in user_inputraw:
        corrected = autocorrect(keyword)
        user_input.append(corrected)
    # this is the auto corrected output
    print user_input


    Sub_distname = ""
    Village = ""
    Officename = ""
    Districtname = ""
    Statename = ""
    StateDict = []
    Districtdict = []
    Sub_distnamedict = []
    pincodes = ""
    # First check if user has given state name and eliminate redundant searching
    for row in reader:
        if len(str(row['StateName']).lower().split()) == 1:
            for keyword in user_input[0:length]:
               if str(row['StateName']).lower() == keyword.lower():
                 Statename = row['StateName'].lower().strip()
                 StateDict.append(row)
        if len(str(row['StateName']).lower().split()) == 2:
            for keyword in user_input[0:length]:
               if str(row['StateName']).lower().split()[0] == keyword.lower():
                 Statename = row['StateName'].lower().strip()
                 StateDict.append(row)
        if len(str(row['StateName']).lower().split()) == 3:
            for keyword in user_input[0:length]:
               if str(row['StateName']).lower().split()[0] == keyword.lower():
                 Statename = row['StateName'].lower().strip()
                 StateDict.append(row)


    #Statename founded and founding pincode in list which corresponds to specific dictionary only

    if Statename != "":

        for item in StateDict:

            for keyword in user_input[0:length]:
                if len(item["Officename"].split()) == 1:
                    if item["Officename"].lower().strip() == keyword.lower():
                        Officename = item["Officename"].lower().strip()
                if len(item["Officename"].split()) == 2:
                    if item["Officename"].lower().strip().split()[0] == keyword.lower():
                        if user_input.index(keyword)+1 < (length) and item["Officename"].lower().strip().split()[1] == user_input[user_input.index(keyword)+1] :
                            Officename = item["Officename"].lower().strip()
                if len(item["Officename"].split()) == 3:
                    if item["Officename"].lower().strip().split()[0] == keyword.lower():
                        if user_input.index(keyword)+1 < (length) and item["Officename"].lower().strip().split()[1] == user_input[user_input.index(keyword)+1]:
                            if user_input.index(keyword)+2 < (length) and item["Officename"].lower().strip().split()[2] == user_input[user_input.index(keyword)+2]:
                                Officename = item["Officename"].lower().strip()

                if len(item["Sub-distname"].split()) == 1:
                    if item["Sub-distname"].lower() == keyword.lower():
                        Sub_distname = item["Sub-distname"].lower().strip()
                if len(item["Sub-distname"].split()) == 2:
                    if item["Sub-distname"].lower().strip().split()[0] == keyword.lower():
                        if user_input.index(keyword)+1 < (length) and item["Sub-distname"].lower().strip().split()[1] == user_input[user_input.index(keyword)+1]:
                            Sub_distname = item["Sub-distname"].lower().strip()
                if len(item["Sub-distname"].split()) == 3:
                    if item["Sub-distname"].lower().strip().split()[0] == keyword.lower():
                        if user_input.index(keyword)+1 < (length) and item["Sub-distname"].lower().strip().split()[1] == user_input[user_input.index(keyword)+1]:
                            if user_input.index(keyword)+2 < (length) and item["Sub-distname"].lower().strip().split()[2] == user_input[user_input.index(keyword) + 2]:
                                Sub_distname = item["Sub-distname"].lower().strip()

                if len(item["Districtname"].split()) == 1:
                    if item["Districtname"].lower() == keyword.lower():
                        Districtname = item["Districtname"].lower().strip()
                if len(item["Districtname"].split()) == 2:
                    if item["Districtname"].lower().strip().split()[0] == keyword.lower():
                        if user_input.index(keyword)+1 < (length) and item["Districtname"].lower().strip().split()[1] == user_input[user_input.index(keyword)+1]:
                            Districtname = item["Districtname"].lower().strip()
                if len(item["Districtname"].split()) == 3:
                    if item["Districtname"].lower().strip().split()[0] == keyword.lower():
                        if user_input.index(keyword)+1 < (length) and item["Districtname"].lower().strip().split()[1] == user_input[user_input.index(keyword) + 1]:
                            if user_input.index(keyword)+2 < (length) and item["Districtname"].lower().strip().split()[2] == user_input[user_input.index(keyword) + 2]:
                                Districtname = item["Districtname"].lower().strip()

        #Officename or  sub_district or district name opr any combination of them is founded and selecting pin code on basis of these info.
        printinfo(Officename,Sub_distname,Districtname,Statename)
        if Districtname != "" and Officename != "":
            for items in StateDict:

                if items["Districtname"].lower().strip() == Districtname and items["Officename"].lower().strip() == Officename:
                    pincodes = items["Pincode"]
                    print pincodes
                    result(pincodes)
                    sys.exit(0)
        if Districtname != "" and Sub_distname != "":
            for items in StateDict:
                if items["Districtname"].lower().strip() == Districtname and items["Sub-distname"].lower().strip() == Sub_distname:
                    pincodes = items["Pincode"]
                    print pincodes
                    result(pincodes)
                    sys.exit(0)
        if Sub_distname != "" and Officename != "":
            for items in StateDict:
                if items["Sub-distname"].lower().strip() == Sub_distname and items["Officename"].lower().strip() == Officename:
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)

        if Sub_distname != "":
            for items in StateDict:
                if items["Sub-distname"].lower().strip() == Sub_distname :
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)
        if Districtname != "":
            for items in StateDict:
                if items["Districtname"].lower().strip() == Districtname:
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)
        if Officename != "":
            for items in StateDict:
                if items["Officename"].lower().strip() == Officename:
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)

    #If Statename not given, Search for districtname and eliminate redundant searching
    reader1 = csv.DictReader(open('Main.csv'))
    if Statename == "":

        for row in reader1:
            #searching if districtname is 1,2 or 3 word long
            if len(str(row['Districtname']).lower().split()) == 1:
                for keyword in user_input[0:length]:
                  if row['Districtname'].lower().strip() == keyword.lower().strip():
                        Districtname = row['Districtname'].lower().strip()
                        Districtdict.append(row)
            if len(str(row['Districtname']).lower().split()) == 2:
               for keyword in user_input[0:length]:
                   if str(row['Districtname']).lower().split()[0] == keyword.lower().strip():
                        Districtname = row['Districtname'].lower().strip()
                        Districtdict.append(row)
            if len(str(row['Districtname']).lower().split()) == 3:
               for keyword in user_input[0:length]:
                   if str(row['Districtname']).lower().split()[0] == keyword.lower().strip():
                       Districtname = row['Districtname'].lower().strip()
                       Districtdict.append(row)

    # districtname found! Search for officename and Sub_distname begins
    # @TODO Can be redundant as 2 word district and sub_distname is not handled till now
    if Districtname != "":
        for item in Districtdict:
            for keyword in user_input[0:length]:
                if item["Officename"].lower().strip() == keyword.lower().strip():
                    Officename = item["Officename"].lower().strip()

                if item["Sub-distname"].lower() == keyword.lower().strip():
                    Sub_distname = item["Sub-distname"].lower().strip()

        printinfo(Officename, Sub_distname, Districtname, Statename)
        if Officename != "":
            for items in Districtdict:
                if items["Officename"].lower().strip() == Officename:
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)

        if Sub_distname != "":
            for items in Districtdict:
                if items["Sub-distname"].lower().strip() == Sub_distname:
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)


        if Sub_distname == "" and Officename == "":
            for items in Districtdict:
                if items["Districtname"].lower().strip() == Districtname:
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)

    #If statename, districtname both unavailable. found on the basis of Sub-distname and officename
    reader2 = csv.DictReader(open('Main.csv'))
    if Statename == "" and Districtname == "":
        for row in reader2:
            if len(str(row['Sub-distname']).lower().split()) == 1:
                # print type(str(row['Sub-distname'].lower().split()))
                for keyword in user_input[0:length]:
                  if row['Sub-distname'].lower().split()[0] == keyword.lower().strip():
                    Sub_distname = row['Sub-distname'].lower().strip()
                    Sub_distnamedict.append(row)

            if len(str(row['Sub-distname']).lower().split()) > 1:
                for keyword in user_input[0:length]:
                   if str(row['Sub-distname']).lower().split()[0].strip() == keyword.lower().strip():
                    if str(row['Sub-distname']).lower().split()[1].strip() == (user_input[user_input.index(keyword) +1]).lower().strip():
                        Sub_distname = row['Sub-distname'].lower().strip()
                        Sub_distnamedict.append(row)
                        print "once"
# case not handled for multiple word officename as its is not necessary at this point
    if Sub_distname != "":
        for item in Sub_distnamedict:
            for keyword in user_input[0:length]:
                if item["Officename"].lower().strip() == keyword.lower().strip():
                        Officename = item["Officename"].lower().strip()
        printinfo(Officename, Sub_distname, Districtname, Statename)
        if Officename != "":
            for items in Sub_distnamedict:
                if items["Officename"].lower().strip() == Officename:
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)

        if Officename == "":
            for items in Sub_distnamedict:
                if items["Sub-distname"].lower().strip() == Sub_distname:
                    pincodes = items["Pincode"]
                    result(pincodes)
                    sys.exit(0)

    # when nothing is given except office name (most refined search. Will give correct output. Search directly from file)
    reader3 = csv.DictReader(open('Main.csv'))
    if Statename == "" and Districtname == "" and Sub_distname == "":

        for row in reader3:
            if len(str(row['Officename']).lower().split()) == length:
              if length == 2:
                for keyword in user_input[0:length]:
                    if str(row['Officename']).lower().split()[0].strip() == keyword.lower().strip():
                        if user_input.index(keyword)+1 < length:
                            if str(row['Officename']).lower().split()[1].strip() == user_input[user_input.index(keyword)+1]:
                                pincodes = row["Pincode"]
                                result(pincodes)
                                sys.exit(0)
              if length == 1:
                for keyword in user_input[0:length]:
                    if str(row['Officename']).lower().split()[0].strip() == keyword.lower().strip():
                                pincodes = row["Pincode"]
                                result(pincodes)
                                sys.exit(0)
              if length == 3:
                for keyword in user_input[0:length]:
                    if str(row['Officename']).lower().split()[0].strip() == keyword.lower():
                        if user_input.index(keyword)+1 < length:
                            if str(row['Officename']).lower().split()[1].strip() == user_input[user_input.index(keyword)+1]:
                                pincodes = row["Pincode"]
                                result(pincodes)
                                sys.exit(0)


    if pincodes == "":

        callwithAPI(user_input)
if __name__ == "__main__":
    main()




# script done except for some cases where ahmed nagar and ambedkar nagar are taken as statename.
# tested on various parameters.

