import re

response = """
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
<title>Malody - Fly Me To The Star 4K Stage Girls&#39; Flight Lv. 15 (vincent4399)</title>
<meta name="description" content="Malody, cross-platform music game community"/>
<meta name="google-site-verification" content="vhjzjuMMc6bdXHGNbmQv5ij1e0US0I1iwOuKIspj14I" />
<meta name="keywords" content="malody, windows, ios, mac, android, game, simulator, ddr, beatmania, iidx, jubeat, osu, lovelive, taiko">
<link rel="shortcut icon" href="/static/favicon.ico" type="image/x-icon"/>
<link rel="stylesheet" type="text/css" href="/static/css/main.css?v=28"/>
<meta name="viewport" content="width=device-width">
<script type="text/javascript" src="/static/js/lib/jquery-2.0.3.min.js?v=2"></script>
<script type="text/javascript" src="/static/js/lib/sea.js"></script>
<script type="text/javascript">
        seajs.config({
                base: '/static/js/'
        });
        var csrftoken = $.cookie('csrftoken');
        function csrfSafeMethod(method) {
                return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }
        $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                                xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                }
        });
        window.malody = window.malody || {};
</script>
<script type="text/javascript">


        </script>
</head>
<body>
<header id="header">
<div class="center">
<span><img src="/static/img/icon-64.png"/><a href="/index">Malody</a></span>
<div class="menu">
<a href="/talk/group"><i class="icon-ta"></i>Talk</a>
<a href="/store/all"><i class="icon-st"></i>Store</a>
<a href="/store/skin"><i class="icon-sk"></i>Skin</a>
<a href="/page/all/chart?type=3"><i class="icon-ch"></i>Chart</a>
<a href="/page/all/player"><i class="icon-pl"></i>Player</a>
</div>
<a href="/accounts/logout">Logout</a>
<a href="/accounts/user/8502"><b>LuiCat</b></a>
<a href="/accounts/user/8502" class="avatar"><img src="http://cni.malody.cn/avatar/8502.png!avatar64" alt="LuiCat" style="max-width:48px;max-height:48px;background:url('');" class="" id="" /></a>
<form action="/page/search" id="J_search_form" class="search g_round">
<input type="text" name="keyword" id="J_search" /><input type="submit" value="" id="J_search_submit"/>
</form>
<div class="notify g_round">
<a href="/talk/user/notify">You have new message(s)</a>
</div>
</div>
</header>
<div id="chead">
<div class="cover" style="background-image:url(http://cni.malody.cn/cover/20598!small?time=1610812700)"></div>
</div>
<div id="center">
<div id="content" class="" style="width:100%">
<link rel="stylesheet" type="text/css" href="/static/css/wiki.css?v=27"/>
<link rel="stylesheet" type="text/css" href="/static/css/tmpl.css?v=16"/>
<div class="song_title g_rblock">
<div class="coverb">
<div class="cover" style="background-image:url(http://cni.malody.cn/cover/20598!small?time=1610812700)"></div>
</div>
<div class="tail">
<a href="/song/20598">Back to song</a>
</div>
<div class="right">
<h2 class="textfix title">
<em class="t0">Alpha</em>
<span class="textfix artist">Revue Starlight Anime Cast</span> - Fly Me To The Star</h2>
<h2 class="mode">
<img src="/static/img/mode/mode-0.png"/>
<span>4K Stage Girls&#39; Flight Lv. 15</span>
<span style="margin-left: 24px">Created by: </span>
<img src="http://cni.malody.cn/avatar/300559!avatar64?time=1585581666" alt="vincent4399" style="max-width:36px;max-height:36px;background:url('');" class="avatar" id="" />
<a href="/accounts/user/300559">vincent4399</a>
<h2 class="sub">
<label>ID</label>:c<span>84548</span>&nbsp;&nbsp;
<label>Length</label>:<span>188s</span>&nbsp;&nbsp;
<label>BPM</label>:<span>124</span>
<label>Last updated</label>:<span class="textfix">2021-01-17 00:00</span>
</h2>
<h2 class="tags">
<span>Tags:</span>
<a href="/page/all/chart?tag=1">4K</a>
<a href="/page/all/chart?tag=15">Custom style</a>
</h2>
</div>
<div class="tool">
<a href="#" class="btn g_toolbtn w" data-type="pubmark" title="Need modification"><i></i></a>
<a href="#" class="btn g_toolbtn e" data-type="edit_meta" title="Edit meta"><i></i></a>
<a href="#" class="btn g_toolbtn d" data-type="del" title="Delete"><i></i></a>
<a href="#" class="btn g_toolbtn m" data-type="merge" title="Merge to another song"><i></i></a>
</div>
</div>
<div class="g_cont2 g_rblock like_area">
<div class="num">
<img src="/static/img/icon-play.png"/><span>Hot</span><span class="l">3</span>
</div>
<div class="num">
<img src="/static/img/icon-love.png"/><span>Recommended</span><span class="l">0</span>
</div>
<div class="num">
<img src="/static/img/icon-bad.png"/><span>Not Recommended</span><span class="l">0</span>
</div>
<div class="line"></div>
<a href="/wiki/1945?cid=84548">Download</a>
</div>
<div class="g_cont2 g_rblock">
<h1 class="sec">Ranking</h1>
<div class="g_actbar" id="score_actbar">
<a href="#" class="g_btn btn" data-type="delmy">Remove score</a>
<select id="g_judge" class="g_options">
<option value="-1">All</option>
<option value="0">A(Easy)</option>
<option value="1">B(Easy+)</option>
<option value="2">C(Normal)</option>
<option value="3">D(Normal+)</option>
<option value="4">E(Hard)</option>
</select>
<select class="g_options" id="g_platform" style="margin-right: 10px">
<option value="0">PC</option>
<option value="1" selected>Mobile</option>
</select>
</div>
<div class="score_area">
<div class="list_head">
<span class="rank">Rank</span>
<span class="name">Player</span>
<span class="score">Score</span>
<span class="combo">Combo</span>
<span class="acc">Acc.</span>
<span class="mod">Mod</span>
<span class="time">Achieved</span>
</div>
<ul class="list">
</ul>
</div>
</div>
<div class="g_cont2 g_rblock">
<div class="tool">
<div class="lang2">
<span>English</span>
<div class="drop">
<div class="list">
<a href="#" data-value="en">English</a>
<a href="#" data-value="sc">简体中文</a>
<a href="#" data-value="tc">繁體中文</a>
<a href="#" data-value="jp">日本語</a>
<a href="#" data-value="kr">한국어</a>
</div>
</div>
</div>
<a href="#" class="btn g_toolbtn e" data-type="edit" title="Edit"><i></i></a>
</div>
<div class="g_wiki">
<div class="g_wiki_new btn" data-type="edit">Add description to the chart</div>
<span class="clear"></span>
</div>
</div>
<div class="g_talk" id="g_talk">
<div id="g_talk_input">
<div class="wrap">
<div class="desc">Notice: You are in public talk, please use English</div>
<div class="tool">
<div class="g_edittool">
<a href="#" data-type="bold"><span title="Bold" class="tool-B" ></span></a>
<a href="#" data-type="italic"><span title="Italic" class="tool-I"></span></a>
<a href="#" data-type="list"><span title="List" class="tool-list"  ></span></a>
<a href="#" data-type="img"><span title="Image" class="tool-img" ></span></a>
<a href="#" data-type="link"><span title="Link" class="tool-link" ></span></a>
<em class="clear"></em>
</div>
<a href="#" class="btn" data-type="cancel" id="J_cancel">X</a>
</div>
<textarea cols="80" rows="30" dir="ltr"></textarea>
<p>
<a class="g_btn btn g_talk_new" data-type="save" id="g_talk_save">Reply</a>
</p>
</div>
</div>
<div class="g_talk_tool">
<div class="g_btn btn g_talk_new" data-type="new"><i></i>Reply</div>
</div>
<ul id="g_talk_list">
</ul>
<div id="g_talk_next" data-type="next" class="talk_btn btn">Show more</div>
<div class="g_talk_new_rep" id="g_talk_new2">
<p>Want to say something?</p>
<div class="g_btn btn g_talk_new" data-type="new"><i></i>Reply</div>
</div>
</div>
<script>
                window.malody = window.malody || {};
                window.malody.wiki = {
                        id: 84548,
                        lang: 1,
                        key: "chart_84548",
                        cid: 84548,
            sid: 20598
                };
                seajs.config({
                        map:[
                                ['wiki/index.js','wiki/index.js?v=13']
                        ]
                });
                seajs.use('module/wiki/index', function (wiki) {
                        wiki.get('./init').init();
                })
        </script>
</div>
<span class="clear"></span>
</div>
<footer id="footer">
<div class="line">
<a href="#">About us</a>
<i></i>
<form action="/i18n/setlang/" method="post">
<input type='hidden' name='csrfmiddlewaretoken' value='Qoh7s24mdDHa2VpQNPrUTO3bHpkny3Cr' />
<input name="next" type="hidden" value="" />
<select name="language" class="g_options">
<option value="zh-hant">
繁體中文
</option>
<option value="zh-hans">
简体中文
</option>
<option value="en" selected="selected">
English
</option>
<option value="ja">
日本語
</option>
</select>
<input class="g_round" type="submit" value="Change" />
</form>
</div>
<span class="copy">Copyright &copy; 2013 ~ 2019 Mugzone</span>
<script>
                window.onresize = function(){
                        if(window.innerHeight > document.body.clientHeight){
                                $('#footer').css("position", "fixed");
                        }else{
                                $('#footer').css('position', 'absolute');
                        }
                };
        </script>
</footer>
<div id="notify">
<div class="msg succ">
<p></p>
</div>
</div>
<div id="login">
<div class="g_title">Sign in<span class="click" data-type="close">X</span></div>
<div class="g_cont">
<h1><label for="s_email">Email</label><input type="text" name="email" id="s_email"/> </h1>
<h1><label for="s_psw">Password</label><input type="password" name="psw" id="s_psw"/> </h1>
<div class="g_btn btn click" data-type="login">Sign in</div>
<h1 style="margin-left: 100px;">
<a href="/accounts/forget">Forgot Password?</a>
<a style="margin-left: 32px; color:#ef6666" href="/accounts/register">Register</a>
</h1>
</div>
<script>
        seajs.config({
                        map:[
                                ['util.js','util.js?v=2']
                        ]
                });
        seajs.use('util', function (util) {
                        util.initLogin();
                })
    </script>
</div>
<div id="g_loading">
<div class="loading"></div>
<span>Wait...</span>
</div>
<div id="analytics">
<script type="text/javascript">
var _bdhmProtocol = (("https:" == document.location.protocol) ? " https://" : " http://");
document.write(unescape("%3Cscript src='" + _bdhmProtocol + "hm.baidu.com/h.js%3F4edad2d5a88ea4e9f4d27e98ccec7300' type='text/javascript'%3E%3C/script%3E"));
</script>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-46796218-2', 'auto');
  ga('send', 'pageview');

</script>
</div>
</body>
</html>
"""

match = re.search(
    "<div class=\"song_title g_rblock\">"
    "\n(?:.*\n)*"
    "<div class=\"tail\">\n"
    "<a href=\"/song/(\d+)\">Back to song</a>\n"
    "(?:.*\n)*"
    "<em class=\"t\d\">([^<]*)</em>\n"
    "<span class=\"textfix artist\">([^<]*)</span> - ([^<]*)</h2>\n"
    "(?:.*\n)*"
    "<img src=\"/static/img/mode/mode-(\d).png\".*\n"
    "<span>([^<]*)</span>(?:\n.*)*Created by:"
    ".*\n.*\n"
    "<a href=\"/accounts/user/(\d+)\">([^<]*)</a>",
    response
)

print(match)
