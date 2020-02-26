# Tensorflow-Telegram-Bot
Telegram Chatbot class which can be used as keras custom callback.
# How to Download
## from source
### 1.git clone https://github.com/Yeachan-Heo/Tensorflow-Telegram-Bot.git
### 2.python setup.py build
### 3.python setup.py install
## via pip
### 1.pip install Tensorflow-Telegram-Bot
# How to use
#### 1.create your Telegram bot and get it's token as explained in https://telegram.org/faq#bots  
#### 2.add your bot as your telegram friend  
#### 3.go to your code, add "from ttb import TelegramBotCallback" at the top 
#### 4.and add TelegramBotCallback(token="your token") to callbacks when calling Model.fit() method.
#### 5.run your code  
#### 6.start your bot  
#### 7.use command /help to learn some commands  
#### 8.enjoy your training  
#### 9.you're welcome XD  

<!DOCTYPE html>
<html>

 <head>

  <meta charset="utf-8"/>
<title>Exported Data</title>
  <meta content="width=device-width, initial-scale=1.0" name="viewport"/>

  <link href="css/style.css" rel="stylesheet"/>

  <script src="js/script.js" type="text/javascript">

  </script>

 </head>

 <body onload="CheckLocation();">

  <div class="page_wrap">

   <div class="page_header">

    <div class="content">

     <div class="text bold">
ych_bot 
     </div>

    </div>

   </div>

   <div class="page_body chat_page">

    <div class="history">

     <div class="message service" id="message-1">

      <div class="body details">
26 February 2020
      </div>

     </div>

     <div class="message service" id="message23908">

      <div class="body details">
History cleared
      </div>

     </div>

     <div class="message default clearfix" id="message23909">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic6" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
y
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:48:53">
20:48
       </div>

       <div class="from_name">
ych_bot 
       </div>

       <div class="text">
hello, yeachan. TensorFlow Telegram Bot is just Started.
       </div>

      </div>

     </div>

     <div class="message default clearfix joined" id="message23910">

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:48:54">
20:48
       </div>

       <div class="text">
Hi, The model is Beginning Training.<br>                          after this, you can get learning status via using some commands<br>                          if you want to know more about that, use command <a href="" onclick="return ShowBotCommand(&quot;help&quot;)">/help</a><br>                          please enjoy your training
       </div>

      </div>

     </div>

     <div class="message default clearfix joined" id="message23911">

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:48:59">
20:48
       </div>

       <div class="text">
invalid command usage
       </div>

      </div>

     </div>

     <div class="message default clearfix joined" id="message23912">

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:49:00">
20:49
       </div>

       <div class="text">
<a href="" onclick="return ShowBotCommand(&quot;help&quot;)">/help</a>: shows this helpful message :D<br>            <a href="" onclick="return ShowBotCommand(&quot;status&quot;)">/status</a>:<br>                usage:<br>                    <a href="" onclick="return ShowBotCommand(&quot;status&quot;)">/status</a> arg1 arg2 arg3....: prints last value of arg1, arg2, arg3<br>                    <a href="" onclick="return ShowBotCommand(&quot;status&quot;)">/status</a> all: prints last value of all arguments<br>            <a href="" onclick="return ShowBotCommand(&quot;plot&quot;)">/plot</a>:<br>                usage:<br>                    <a href="" onclick="return ShowBotCommand(&quot;plot&quot;)">/plot</a> arg1 arg2 arg3....: plots all value of arg1, arg2, arg3 in one figure<br>                    <a href="" onclick="return ShowBotCommand(&quot;plot&quot;)">/plot</a> all: plots all value of all argument in one figure<br>            <a href="" onclick="return ShowBotCommand(&quot;set&quot;)">/set</a>:<br>                usage:<br>                    <a href="" onclick="return ShowBotCommand(&quot;set&quot;)">/set</a> lr: changes learning rate<br>            if you can&apos;t get it, why don&apos;t you just try?
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23913">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic4" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
yH
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:49:40">
20:49
       </div>

       <div class="from_name">
yeachan Hue
       </div>

       <div class="text">
<a href="" onclick="return ShowBotCommand(&quot;status&quot;)">/status</a> all
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23914">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic6" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
y
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:49:42">
20:49
       </div>

       <div class="from_name">
ych_bot 
       </div>

       <div class="text">
loss:0.22736297063231467<br>accuracy:0.9146166443824768<br>val_loss:0.3432700324833393<br>val_accuracy:0.8823999762535095<br>epoch:11
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23915">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic4" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
yH
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:49:51">
20:49
       </div>

       <div class="from_name">
yeachan Hue
       </div>

       <div class="text">
<a href="" onclick="return ShowBotCommand(&quot;status&quot;)">/status</a> loss val_loss
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23916">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic6" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
y
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:49:53">
20:49
       </div>

       <div class="from_name">
ych_bot 
       </div>

       <div class="text">
loss:0.20499075312862794<br>val_loss:0.3357230696260929
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23917">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic4" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
yH
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:50:08">
20:50
       </div>

       <div class="from_name">
yeachan Hue
       </div>

       <div class="text">
<a href="" onclick="return ShowBotCommand(&quot;status&quot;)">/status</a> accuracy val_accuracy
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23918">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic6" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
y
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:50:13">
20:50
       </div>

       <div class="from_name">
ych_bot 
       </div>

       <div class="text">
accuracy:0.9316333532333374<br>val_accuracy:0.8859999775886536
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23919">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic4" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
yH
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:50:38">
20:50
       </div>

       <div class="from_name">
yeachan Hue
       </div>

       <div class="text">
<a href="" onclick="return ShowBotCommand(&quot;plot&quot;)">/plot</a> loss val_loss
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23920">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic6" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
y
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:50:40">
20:50
       </div>

       <div class="from_name">
ych_bot 
       </div>

       <div class="text">
drawing plot
       </div>

      </div>

     </div>

     <div class="message default clearfix joined" id="message23921">

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:50:41">
20:50
       </div>

       <div class="media_wrap clearfix">

        <a class="photo_wrap clearfix pull_left" href="photos/photo_1@26-02-2020_20-50-41.jpg">

         <img class="photo" src="photos/photo_1@26-02-2020_20-50-41_thumb.jpg" style="width: 260px; height: 195px"/>

        </a>

       </div>

      </div>

     </div>

     <div class="message default clearfix joined" id="message23922">

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:50:42">
20:50
       </div>

       <div class="text">
here&apos;s your plot!
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23923">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic4" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
yH
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:50:59">
20:50
       </div>

       <div class="from_name">
yeachan Hue
       </div>

       <div class="text">
<a href="" onclick="return ShowBotCommand(&quot;plot&quot;)">/plot</a> accuracy val_accuracy
       </div>

      </div>

     </div>

     <div class="message default clearfix" id="message23924">

      <div class="pull_left userpic_wrap">

       <div class="userpic userpic6" style="width: 42px; height: 42px">

        <div class="initials" style="line-height: 42px">
y
        </div>

       </div>

      </div>

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:51:01">
20:51
       </div>

       <div class="from_name">
ych_bot 
       </div>

       <div class="text">
drawing plot
       </div>

      </div>

     </div>

     <div class="message default clearfix joined" id="message23925">

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:51:03">
20:51
       </div>

       <div class="media_wrap clearfix">

        <a class="photo_wrap clearfix pull_left" href="photos/photo_2@26-02-2020_20-51-03.jpg">

         <img class="photo" src="photos/photo_2@26-02-2020_20-51-03_thumb.jpg" style="width: 260px; height: 195px"/>

        </a>

       </div>

      </div>

     </div>

     <div class="message default clearfix joined" id="message23926">

      <div class="body">

       <div class="pull_right date details" title="26.02.2020 20:51:03">
20:51
       </div>

       <div class="text">
here&apos;s your plot!
       </div>

      </div>

     </div>

    </div>

   </div>

  </div>

 </body>

</html>
