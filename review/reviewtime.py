from datetime import datetime,timedelta

def review_time(today):
    delta_list = [1,1,2,2,3,4,5,5]
    review_day = []
    new_day = datetime.strptime(today, '%m-%d')
    for day in delta_list:
        new_day = datetime.strptime(new_day.strftime('%m-%d'),'%m-%d') + timedelta(days=day)
        review_day.append(new_day.strftime('%m.%d'))
    print('today is ', today, 'review days are', review_day)

if __name__=='__main__':
    day = input('review day:')
    print(day)
    review_time(day)