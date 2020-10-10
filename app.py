from flask import Flask,request,send_from_directory
from flask import render_template
import datetime,os
app = Flask(__name__)
class jisuan_class():
    def __init__(self,canyuliang,date):
        self.render_datas={};
        self.canyuliang=float(canyuliang);
        self.date = datetime.datetime.strptime(date, '%Y-%m-%d')
    def comput_datas(self):
        #     家庭
        fenzhong = [4 * 60, 6 * 60, 8 * 60, 10 * 60, 12 * 60]
        self.shuju_s('jiating',"与家庭成员接触",1,fenzhong,is_xiaoshi=True);
        #   儿童
        fenzhong = [5, 10, 15, 30, 60]
        self.shuju_s('ertong',"与儿童接触",0.1,fenzhong,is_xiaoshi=False);
        # 睡觉
        fenzhong = [8 * 60, 10 * 60]
        self.shuju_s('shuijiao',"睡觉接触", 0.3, fenzhong, is_xiaoshi=True);
        # 同事
        fenzhong = [4 * 60, 6 * 60, 8 * 60, 10 * 60, 12 * 60]
        self.shuju_s('tongshi',"与同事接触", 1, fenzhong, is_xiaoshi=True);
        # 公交
        fenzhong = [1 * 60, 1.5 * 60, 2 * 60, 3 * 60]
        self.shuju_s('gongjiao',"公交接触", 0.1, fenzhong, is_xiaoshi=True);
        # 旅游
        fenzhong = [4 * 60, 6 * 60, 8 * 60, 10 * 60, 12 * 60]
        self.shuju_s('lvyou',"旅游接触", 0.1, fenzhong, is_xiaoshi=True);
        #解除限制时间
        fenzhong = [4 * 60, 8 * 60, 12 * 60]
        self.shuju_s('jiechuxianzhi', "解除限制时间", 0.1, fenzhong, is_xiaoshi=True);
        return self.render_datas
    def shuju_s(self,key,miaoshu,juli,shijian_fen_list,is_xiaoshi):
        self.render_datas[key]=[];
        for i in shijian_fen_list:
            if(key in ("lvyou",'gongjiao')):
                now_date = self.date + datetime.timedelta(days=self.danciijichuxianzhi_hh(self.canyuliang, juli, i));
            else:
                now_date= self.date + datetime.timedelta(days=self.jiechuxianzhi_hh(self.canyuliang, juli, i));
            if(is_xiaoshi):
                xiaoshi = self.fen_to_xiaoshi(i);
                self.render_datas[key].append([str(xiaoshi) + "小时", str(juli)+'米', now_date.strftime('%Y-%m-%d')])
            else:
                self.render_datas[key].append([str(i) + "分钟", str(juli)+'米', now_date.strftime('%Y-%m-%d')])
        self.render_datas[key].append(miaoshu);

    def danciijichuxianzhi_hh(self,canyuliang, juli, jiechufenzhong):
        tianshu = 0;
        while True:
            tianshu += 1;
            if ((canyuliang * 2.157/ pow(juli, 1.5) / 1000)*jiechufenzhong/60 < 1):
                break
            canyuliang = canyuliang * 0.9094;
            if (tianshu > 10000): break
        return tianshu - 1;
    def jiechuxianzhi_hh(self,canyuliang, juli, jiechufenzhong):
        tianshu = 0;
        while True:
            tianshu += 1;
            if ((canyuliang * 0.0227 * jiechufenzhong / pow(juli, 1.5) / 60) < 1):
                break
            canyuliang = canyuliang * 0.9094;
            if (tianshu > 10000): break
        return tianshu - 1;

    def fen_to_xiaoshi(self,fen):
        return fen / 60
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'down.png', mimetype='image/vnd.microsoft.icon')
@app.route('/xuzhi')
def xuzhi():
    return render_template("xuzhi.html")
@app.route('/')
def hello_world():
    return render_template("index.html")
@app.route('/tc')
def tc_time():
    return render_template("tc.html")
#
@app.route('/jisuan',methods=['POST'])
def jisuan():
    post_data=request.form
    riqi=post_data.get('riqi')
    canyuliang=post_data.get('canzhi')
    js=jisuan_class(canyuliang,riqi);
    return render_template("jieguo.html",datas=js.comput_datas(),len=len,range=range,list=list)

if __name__ == '__main__':
    # app.run();
    app.run(host="0.0.0.0",
            port=5000,
            debug=True)
