from roboter import console
from roboter import ranking

ROBOT_NAME='ROBOTA'

class Robot(object):
    def __init__(self,robot_name=ROBOT_NAME,user_name='',color='green'):
        self.robot_name=robot_name
        self.user_name=user_name
        self.color=color

    def hello(self):
        while True:
            template=console.get_template('hello.txt',self.color)
            user_name=input(template.substitute({'robot_name':self.robot_name}))

            if user_name:
                self.user_name=user_name.title()
                break

class RestaurantRobot(Robot):
    def __init__(self,name=ROBOT_NAME):
        super().__init__(robot_name=name)
        self.ranking_model=ranking.RankingModel()

    def _hello_decorator(func):
        def wrapper(self):
            if not self.user_name:
                self.hello()
            return func(self)
        return wrapper

    @_hello_decorator
    def recommend_restaurant(self):
        new_recommend_restaurant=self.ranking_model.get_most_popular()
        if not new_recommend_restaurant:
            return None
        will_recommend_restaurants=[new_recommend_restaurant]
        while True:
            template=console.get_template('recommend.txt',self.color)
            answer = input(template.substitute({
                'restaurant':new_recommend_restaurant
            }))
            if answer.lower()=='y' or answer.lower()=='yes':
                break
            if answer.lower()=='n' or answer.lower()=='no':
                new_recommend_restaurant=self.ranking_model.get_most_popular(not_list=will_recommend_restaurants)
                if not new_recommend_restaurant:
                    break
                will_recommend_restaurants.append(new_recommend_restaurant)

    @_hello_decorator
    def ask_user_favorite(self):
        while True:
            template = console.get_template('ask.txt',self.color)
            restaurant = input(template.substitute({
                'robot_name':self.robot_name,
                'user_name':self.user_name
            }))
            if restaurant:
                self.ranking_model.increment(restaurant)
                break

    @_hello_decorator
    def thank_you(self):
        template=console.get_template('bye.txt',self.color)
        print(template.substitute({
            'robot_name':self.robot_name,
            'user_name':self.user_name
        }))
