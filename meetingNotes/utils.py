import csv
import math
import requests
import os
import pandas
import plotly.express as px
import shutil
from datetime import datetime, date, timedelta
import openai
import numpy as np
from collections import defaultdict
import pandas as pd
import re

debug = False

mcd = {}
nrc = {}

def saveTextAsCsv(text, timestamp):
   counts = defaultdict(int)
   for word in re.findall('\w+', text):
       counts[word] += 1

   df = pd.DataFrame.from_dict(counts, orient='index', columns=['value'])
   df.to_csv(timestamp + '.csv', index=True)

def loadMcDonald():
    global mcd
    if len(mcd) > 0 :
        print('mcd was already loaded...')
        return mcd

    print('downloading MCD dictionary...')
    spreadSheetURL = 'https://docs.google.com/spreadsheets/d/13ke_m'
    response = requests.get(url=spreadSheetURL)
    assert response.status_code == 200, 'Error'
    print('MCD dictionary downloaded.')
    open('McDonald.csv', 'w+').write(response.content.decode('utf-8-sig'))

    resultDict = {}
    with open('McDonald.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        headers = []
        for row in csv_reader:
            headers = row
            break

        for row in csv_reader:
        
            resultDict[row[0].lower()] = {}

            k = 0
            for header in headers:
                if k == 0:
                    k = k + 1
                    continue
                resultDict[row[0].lower()][header.lower()] = row[k].replace(',', '.')
                k = k + 1
        mcd = resultDict
        return resultDict


def loadNRC():
    global nrc
    if len(nrc) > 0 :
        print('nrc was already loaded...')
        return nrc

    print('downloading NRC dictionary...')
    spreadSheetURL = 'https://docs.goog'
    response = requests.get(url=spreadSheetURL)
    assert response.status_code == 200, 'Error'
    print('NRC dictionary downloaded')
    open('NRC.csv', 'w+').write(response.content.decode('utf-8-sig'))

    resultDict = {}
    with open('NRC.csv', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            word = row[0].lower()

            if word not in resultDict:
                resultDict[word] = {}
            emotion = row[1]
            value = row[2]
            resultDict[word][emotion] = value
        
        nrc = resultDict
        return resultDict


# json_body = json.dumps(loadMcDonald(), indent = 4)
# print(json_body)


# json_body = json.dumps(loadNRC(), indent = 4)
# print(json_body)

def loadOutputWordsInSound(timestamp):
    with open(timestamp + '.csv', encoding='utf-8-sig') as csv_file:
        resultDict = {}
        csv_reader = csv.reader(csv_file, delimiter=',')

        i = 0
        for row in csv_reader:
            if i == 0:
               i = i +1 
               continue
            word = row[0].lower()
            count = row[1]
            resultDict[word] = count
    
    return resultDict

def calculateValuesForFile(timestamp):
    words = loadOutputWordsInSound(timestamp)
    nrc = loadNRC()
    mc_donald = loadMcDonald()

    file = open(timestamp +  '_output.csv', 'w')
    writer = csv.writer(file)
    headers = ['word_in_text', 'count', 'sum', 
    'sent_level', 'mcd_negative', 'mcd_positive', 
    'uncertainty', 'litigious', 'strong_modal', 
    'weak_modal', 'constraining', 'fear',
    'anger', 'anticipation','trust',
    'surprise','nrc_positive','nrc_negative',
    'sadness','disgust','joy']
    writer.writerow(headers)

    all_sum = 0
    all_sent_level = 0
    all_sent_level_positive = 0
    all_sent_level_negative = 0
    all_mcd_negative = 0
    all_mdc_positive = 0
    all_uncertainty = 0
    all_litigious = 0
    all_strong_modal = 0
    all_weak_modal = 0
    all_constraining = 0

    all_fear = 0
    all_anger = 0
    all_anticipation = 0
    all_trust = 0
    all_surprise = 0
    all_nrc_positive = 0
    all_nrc_negative = 0
    all_sadness = 0
    all_disgust = 0
    all_joy = 0

    for word in words:
        if word in mc_donald.keys() and word in nrc.keys() :
            count = words[word]
            
            if debug:
                print(word)

            mc_donald_instance = mc_donald[word]
            sum = mc_donald_instance['sum']
            all_sum += float(sum)

            sent_level = float(sum) * (math.log(float(count), 10) + 1)
            all_sent_level += sent_level
            if sent_level > 0:
                all_sent_level_positive += sent_level
            else:
                all_sent_level_negative += sent_level

            mcd_negative = mc_donald_instance['negative']
            all_mcd_negative += float(mcd_negative)

            mcd_positive = mc_donald_instance['positive']
            all_mdc_positive += float(mcd_positive)

            uncertainty = mc_donald_instance['uncertainty']
            all_uncertainty += float(uncertainty)

            litigious = mc_donald_instance['litigious']
            all_litigious += float(litigious)

            strong_modal = mc_donald_instance['strong_modal']
            all_strong_modal += float(strong_modal)

            weak_modal = mc_donald_instance['weak_modal']
            all_weak_modal += float(weak_modal)

            constraining = mc_donald_instance['constraining']
            all_constraining += float(constraining)

            if debug:
                print(sum)
                print(sent_level)
                print(mcd_negative)
                print(mcd_positive)
                print(uncertainty)
                print(litigious)
                print(strong_modal)
                print(weak_modal)
                print(constraining)

            fear = 0
            anger = 0
            anticipation = 0
            trust = 0
            surprise = 0
            nrc_positive = 0
            nrc_negative = 0
            sadness = 0
            disgust = 0
            joy = 0
            
            if 'fear' in nrc[word]:
                fear =  0 if nrc[word]['fear'] == '0' else sent_level * float(nrc[word]['fear'])
            if 'anger' in nrc[word]:
                anger = 0 if nrc[word]['anger'] == '0' else sent_level * float(nrc[word]['anger'])
            if 'anticipation' in nrc[word]:
                anticipation = 0 if nrc[word]['anticipation'] == '0' else sent_level * float(nrc[word]['anticipation'])
            if 'trust' in nrc[word]:
                trust = 0 if nrc[word]['trust'] == '0' else sent_level * float(nrc[word]['trust'])
            if 'surprise' in nrc[word]:
                surprise = 0 if nrc[word]['surprise'] == '0' else sent_level * float(nrc[word]['surprise'])
            if 'positive' in nrc[word]:
                nrc_positive = 0 if nrc[word]['positive'] == '0' else sent_level * float(nrc[word]['positive'])
            if 'negative' in nrc[word]:
                nrc_negative = 0 if nrc[word]['negative'] == '0' else sent_level * float(nrc[word]['negative'])
            if 'sadness' in nrc[word]:
                sadness = 0 if nrc[word]['sadness'] == '0' else sent_level * float(nrc[word]['sadness'])
            if 'disgust' in nrc[word]:
                disgust = 0 if nrc[word]['disgust'] == '0' else sent_level * float(nrc[word]['disgust'])
            if 'joy' in nrc[word]:
                joy = 0 if nrc[word]['joy'] == '0' else sent_level * float(nrc[word]['joy'])

            all_fear += float(fear)
            all_anger += float(anger)
            all_anticipation += float(anticipation)
            all_trust += float(trust)
            all_surprise += float(surprise)
            all_nrc_positive += float(nrc_positive)
            all_nrc_negative += float(nrc_negative)
            all_sadness += float(sadness)
            all_disgust += float(disgust)
            all_joy += float(joy)


            if debug:
                print(fear)
                print(anger)
                print(anticipation)
                print(trust)
                print(surprise)
                print(nrc_negative)
                print(nrc_positive)
                print(sadness)
                print(disgust)
                print(joy)

            data = [word, count, sum, 
            sent_level, mcd_negative, mcd_positive, 
            uncertainty, litigious, strong_modal, 
            weak_modal, constraining, fear,
            anger, anticipation, trust,
            surprise, nrc_positive, nrc_negative,
            sadness, disgust, joy]

            writer.writerow(data)
        else:

            count = words[word]
            
            if debug:
                print(word)
            sum = 0
            sent_level = 0

            mcd_negative = 0

            mcd_positive = 0

            uncertainty = 0

            litigious = 0

            strong_modal = 0

            weak_modal = 0

            constraining = 0

            if debug:
                print(sum)
                print(sent_level)
                print(mcd_negative)
                print(mcd_positive)
                print(uncertainty)
                print(litigious)
                print(strong_modal)
                print(weak_modal)
                print(constraining)

            fear = 0
            anger = 0
            anticipation = 0
            trust = 0
            surprise = 0
            nrc_positive = 0
            nrc_negative = 0
            sadness = 0
            disgust = 0
            joy = 0
            
            data = [word, count, sum, 
            sent_level, mcd_negative, mcd_positive, 
            uncertainty, litigious, strong_modal, 
            weak_modal, constraining, fear,
            anger, anticipation, trust,
            surprise, nrc_positive, nrc_negative,
            sadness, disgust, joy]

            writer.writerow(data)
    file.close()

    file = open(timestamp + '_output_total.csv', 'w')
    writer = csv.writer(file)
    headers = ['Sentiment', 'Value', 'Size']
    writer.writerow(headers)

    if int(all_sent_level) != 0:
        writer.writerow(['Overall Sentiment', all_sent_level, abs(all_sent_level)])
    
    if int(all_sent_level_positive) != 0:
        writer.writerow(['Positive Sentiment', all_sent_level_positive, abs(all_sent_level_positive)])
    
    if int(all_sent_level_negative) != 0:
        writer.writerow(['Negative Sentiment', all_sent_level_negative, abs(all_sent_level_negative)])

    if int(all_uncertainty) != 0:
        writer.writerow(['Uncertainty', all_uncertainty, abs(all_uncertainty)])
    
    if int(all_litigious) != 0:
        writer.writerow(['Litigation', all_litigious, abs(all_litigious)])

    if int(all_fear) != 0:
        writer.writerow(['Fear', all_fear, abs(all_fear)])

    if int(all_anger) != 0:
        writer.writerow(['Anger', all_anger, abs(all_anger)])

    if int(all_anticipation) != 0:
        writer.writerow(['anticipation', all_anticipation, abs(all_anticipation)])

    if int(all_trust) != 0:
        writer.writerow(['Trust', all_trust, abs(all_trust)])

    if int(all_surprise) != 0:
        writer.writerow(['Surprise', all_surprise, abs(all_surprise)])

    if int(all_sadness) != 0:
        writer.writerow(['Sadness', all_sadness, abs(all_sadness)])

    if int(all_disgust) != 0:
        writer.writerow(['Disgust', all_disgust, abs(all_disgust)])

    if int(all_joy) != 0:
        writer.writerow(['Joy', all_joy, abs(all_joy)])
    file.close()

def drawAndSaveDiagram(timestamp):
    df = pandas.read_csv(timestamp + '_output_total.csv', sep=",")
    df = df.sort_values(by ='Value',ascending=True)
    
    print(df)
    # fig = px.scatter(df, x="Value", y="Value",size="Size", color="Sentiment",hover_name="Sentiment", log_x=False, size_max=30)
    fig = px.bar(df, x='Sentiment', y='Value', color="Value", color_discrete_sequence=px.colors.sequential.Plasma_r[0:len(df)])

    fig.write_image(timestamp + '_diagram.jpg')
    
def copyFileToPublishedDateLocation(channelId, videoId, videoPublishedDate):
    publishedDate = datetime.strptime(videoPublishedDate, "%Y-%m-%dT%H:%M:%SZ")
    publishedDate = str(publishedDate.date())
    
    try:
        os.mkdir(publishedDate)
    except OSError as error:
        print(error) 
        pass

    try:
        os.mkdir(publishedDate + '/' + channelId)
    except OSError as error:
        print(error)
        pass

    try:
        os.mkdir(publishedDate + '/' + channelId + '/' + videoId)
    except OSError as error:
        print(error)
        pass

    try:
        shutil.copyfile(channelId + '/' + videoId + '/' + videoId + '_output_total.csv', publishedDate + '/' + channelId + '/' + videoId + '/' + videoId + '_output_total.csv')
    except Exception as error:
        print(error)
        pass

def calculateTotalsPerChannel():
    print('sending totals per day to channel...')
    yesterday = str(date.today() - timedelta(days = 1))

    try:

        channels = [d for d in os.listdir(yesterday) if os.path.isdir(os.path.join(yesterday, d))]
        for channelId in channels:
            channelSumDict = {}
            keys = []
            videos = [d for d in os.listdir(yesterday + '/' + channelId) if os.path.isdir(os.path.join(yesterday + '/' + channelId, d))]

            for videoId in videos:
                csvLocation = yesterday + '/' + channelId + '/' + videoId + '/' + videoId + '_output_total.csv'
                with open(csvLocation, encoding='utf-8-sig') as csv_file:
                    csv_reader = csv.reader(csv_file, delimiter=',')
                    i = 0
                    for row in csv_reader:
                        if i == 0:
                            i = i +1
                            continue

                        key = row[0]
                        value = row[1]
                        size = row[2]

                        if key not in keys:
                            keys.append(key)

                        if key + 'value' not in channelSumDict and key + 'size' not in channelSumDict:
                            channelSumDict[key + 'value'] = float(value)
                            channelSumDict[key + 'size'] = float(size)
                        else:
                            channelSumDict[key + 'value'] = round(channelSumDict[key + 'value'] + float(value), 2)
                            channelSumDict[key + 'size'] = round(channelSumDict[key + 'size'] + float(size), 2)

            file = open(yesterday + '/' + channelId + '/total.csv', 'w')
            writer = csv.writer(file)
            headers = ['Sentiment', 'Value', 'Size']
            writer.writerow(headers)
            for key in keys:
                row = [key, channelSumDict[key + 'value'], channelSumDict[key + 'size']]
                writer.writerow(row)
            file.close()

            df = pandas.read_csv(yesterday + '/' + channelId + '/total.csv', sep=",")
            df = df.sort_values(by ='Value',ascending=True)
            
            # fig = px.scatter(df, x="Value", y="Value",size="Size", color="Sentiment",hover_name="Sentiment", log_x=False, size_max=30)
            fig = px.bar(df, x='Sentiment', y='Value', color="Value", color_discrete_sequence=px.colors.sequential.Plasma_r[0:len(df)])

            fig.write_image(yesterday + '/' + channelId + '/diagram.jpg')
    except Exception as error:
        print(error)
        pass

    return yesterday

def getVideoDescriptionFromText(text):
    try:
        # https://colab.research.google.com/drive/15tr9FMCDuSO5Dahw8XMEkk2-p4CoR17s?usp=sharing
        print('getting video description...')

        openai.api_key = 'sk'
        words = text.split(" ")
        print(math.ceil(len(words)/2000))
        chunks = np.array_split(words, math.ceil(len(words)/2000))
        sentences = ' '.join(list(chunks[0]))

        summary_responses = []

        for chunk in chunks:
            sentences = ' '.join(list(chunk))
            prompt = f"{sentences}\n\ntl;dr:"

            response = openai.Completion.create(
                engine="text-davinci-003", 
                prompt=prompt,
                temperature=0.3, # The temperature controls the randomness of the response, represented as a range from 0 to 1. A lower value of temperature means the API will respond with the first thing that the model sees; a higher value means the model evaluates possible responses that could fit into the context before spitting out the result.
                max_tokens=150,
                top_p=1, # Top P controls how many random results the model should consider for completion, as suggested by the temperature dial, thus determining the scope of randomness. Top P’s range is from 0 to 1. A lower value limits creativity, while a higher value expands its horizons.
                frequency_penalty=0,
                presence_penalty=1
            )

            response_text = response["choices"][0]["text"]
            summary_responses.append(response_text)

            full_summary = "".join(summary_responses)
            # print(full_summary)


        #print("video summary")
        #print(full_summary)
        return full_summary
    except Exception as e:
        print(e)
        return str(e)




