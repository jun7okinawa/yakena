#!/usr/bin/perl

#┌─────────────────────────────────
#│ POST-MAIL v3.41 (2006/03/23)
#│ copyright (c) KentWeb
#│ webmaster@kent-web.com
#│ http://www.kent-web.com/
#└─────────────────────────────────
$ver = 'postmail v3.41';
#┌─────────────────────────────────
#│ [注意事項]
#│ 1. このスクリプトはフリーソフトです。このスクリプトを使用した
#│    いかなる損害に対して作者は一切の責任を負いません。
#│ 2. 送信フォームのHTMLページの作成に関しては、HTML文法の範疇
#│    となるため、サポート対象外となります。
#│ 3. 設置に関する質問はサポート掲示板にお願いいたします。
#│    直接メールによる質問はお受けいたしておりません。
#└─────────────────────────────────
#
# [ 送信フォーム (HTML) の記述例 ]
#
# ・タグの記述例 (1)
#   おなまえ <input type=text name="name" size=25>
#   → このフォームに「山田太郎」と入力して送信すると、
#      「name = 山田太郎」という形式で受信します
#
# ・タグの記述例 (2)
#   お好きな色 <input type=radio name="color" value="青">
#   → このラジオボックスにチェックして送信すると、
#      「color = 青」という形式で受信します
#
# ・タグの記述例 (3)
#   E-mail <input type=text name="email" size=25>
#   → name値に「email」という文字を使うとこれはメールアドレス
#      と認識し、アドレスの書式を簡易チェックします
#   → (○) abc@xxx.co.jp
#   → (×) abc.xxx.co.jp → 入力エラーとなります
#
# ・タグの記述例 (4)
#   E-mail <input type=text name="_email" size=25>
#   → name値の先頭に「アンダーバー 」を付けると、その入力値は
#     「入力必須」となります。
#      上記の例では、「メールアドレスは入力必須」となります。
#
# ・name値への「全角文字」の使用は可能です
#  (例) <input type=radio name="年齢" value="20歳代">
#  → 上記のラジオボックスにチェックを入れて送信すると、
#     「年齢 = 20歳代」という書式で受け取ることができます。
#
# ・mimew.pl使用時、name値を「name」とするとこれを「送信者名」と認識
#   して送信元のメールアドレスを「送信者 <メールアドレス>」という
#   フォーマットに自動変換します。
#  (フォーム記述例)  <input type=text name="name">
#  (送信元アドレス)  太郎 <taro@email.xx.jp>
#
# ・コマンドタグ (1)
#   → 入力必須項目を強制指定する（半角スペースで複数指定可）
#   → ラジオボタン、チェックボックス対策
#   → name値を「need」、value値を「必須項目1 + 半角スペース +必須項目2 + 半角スペース ...」
#   (例) <input type=hidden name="need" value="名前 メールアドレス 性別">
#
# ・コマンドタグ (2)
#   → 2つの入力内容が同一かをチェックする
#   → name値を「match」、value値を「項目1 + 半角スペース + 項目2」
#   (例) <input type=hidden name="match" value="email email2">
#
# ・コマンドタグ (3)
#   → メール件名を指定する
#   → この場合、設定で指定する $subject より優先されます。
#   (例) <input type=hidden name="subject" value="メールタイトル○○">
#
#  [ 簡易チェック ]
#   http://～～/postmail.cgi?mode=check
#
#  [ 設置例 ]
#
#  public_html / index.html (トップページ等）
#       |
#       +-- postmail / postmail.cgi  [705]
#                      jcode.pl      [604]
#                      mimew.pl      [604] ... 任意
#                      postmail.html
#                      tmp_*.html ... テンプレートファイル

#-------------------------------------------------
#  ▼基本設定
#-------------------------------------------------

# 文字コード変換ライブラリ
require './jcode.pl';

# MIMEエンコードライブラリを使う場合（推奨）
#  → メールヘッダの全角文字をBASE64変換する機能
#  → mimew.plを指定
$mimew = './mimew.pl';

# メールソフトまでのパス
#  → sendmailの例 ：/usr/lib/sendmail
#  → BlatJの例    ：c:\blatj\blatj.exe
$mailprog = '/usr/sbin/sendmail';

# 送信先メールアドレス
$mailto = 'kayakclubgoodlife@gmail.com';

# 入力フィールドあたりの最大容量（バイト）
# ＊参考 : 全角1文字 = 2バイト
$max_field = 800;

# 送信前確認
#  0 : no
#  1 : yes
$preview = 0;

# メールタイトル
$subject = 'フォームメール';

# 本体プログラムURL
$script = './postmail.cgi';

# 確認画面テンプレート
$tmp_conf = './tmp_conf.html';

# 一般エラー画面テンプレート
$tmp_err1 = './tmp_err1.html';

# 入力エラー画面テンプレート
$tmp_err2 = './tmp_err2.html';

# 送信後画面テンプレート
$tmp_thx = './tmp_thx.html';

# 送信後の形態
#  0 : 完了メッセージを出す.
#  1 : 戻り先 ($back) へ自動ジャンプさせる.
$reload = 1;

# 送信後の戻り先
#  → http://から記述する
$back = 'http://www.go-goodlife.com/thx.html';

# 送信は method=POST 限定 (0=no 1=yes)
#  → セキュリティ対策
$postonly = 1;

# アラーム色
$alm_col = "#dd0000";

# ホスト取得方法
# 0 : gethostbyaddr関数を使わない
# 1 : gethostbyaddr関数を使う
$gethostbyaddr = 0;

# 送信元へ控え (CC) を送る
# 0=no 1=yes
# ＊セキュリティ上この機能は推奨しません.
# ＊name="email" のフィールドへの入力が必須となります.
$cc_mail = 0;

#-------------------------------------------------
#  ▲設定完了
#-------------------------------------------------

# フォームデコード
$ret = &decode;

# 基本処理
if (!$ret) { &error("不明な処理です"); }
elsif ($in{'mode'} eq "check") { &check; }

# POSTチェック
if ($postonly && !$postflag) { &error("不正なアクセスです"); }

# 汚染チェック
if ($in{'subject'} =~ /\r|\n/) { &error("メール件名が不正です"); }
$in{'subject'} =~ s/\@/＠/g;
$in{'subject'} =~ s/\./．/g;
$in{'subject'} =~ s/\+/＋/g;
$in{'subject'} =~ s/\-/－/g;
$in{'subject'} =~ s/\:/：/g;
$in{'subject'} =~ s/\;/；/g;
$in{'subject'} =~ s/\|/｜/g;

# メールプログラムの種類チェック
if ($mailprog =~ /blat/i) { $pgType = 2; } else { $pgType = 1; }

# 著作権表記（削除不可）
$copy = <<EOM;
<br><br><div align="center">
<span style="font-size:10px;font-family:Verdana,Helvetica,Arial;">
- <a href="http://www.kou-s.co.jp/" target="_top"></a> -
</span></div>
EOM

# 必須入力チェック
if ($in{'need'}) {
	local(@tmp, @uniq, %seen);

	# needフィールドの値を必須配列に加える
	@tmp = split(/\s+/, $in{'need'});
	push(@need,@tmp);

	# 必須配列の重複要素を排除する
	foreach (@need) {
		push(@uniq,$_) unless $seen{$_}++;
	}

	# 必須項目の入力値をチェックする
	foreach (@uniq) {

		# フィールドの値が投げられてこないもの（ラジオボタン等）
		if (!defined($in{$_})) {
			$check++;
			push(@key,$_);
			push(@err,$_);

		# 入力なしの場合
		} elsif ($in{$_} eq "") {
			$check++;
			push(@err,$_);
		}
	}
}

# 入力内容マッチ
if ($in{'match'}) {
	($match1,$match2) = split(/\s+/, $in{'match'}, 2);

	if ($in{$match1} ne $in{$match2}) {
		&error("$match1と$match2の再入力内容が異なります");
	}
}

# 入力チェック確認画面
if ($check || $max_flg) { &err_check; }

# E-Mail書式チェック
if ($in{'email'} =~ /\,/) {
	&error("メールアドレスにコンマ ( , ) が含まれています");
}
if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
	&error("メールアドレスの書式が不正です");
}

# プレビュー
if ($preview && $in{'mode'} ne "send") {

	local($cp_flag,$flag,$cell,$tmp);
	open(IN,"$tmp_conf") || &error("Open Error: $tmp_conf");
	print "Content-type: text/html\n\n";
	while (<IN>) {
		if (/<!-- cell_begin -->/) {
			$flag=1;
		}
		if (/<!-- cell_end -->/) {
			$flag=0;

			local($key,$bef,$tmp);

			print "<input type=hidden name=mode value=send>\n";

			foreach $key (@key) {
				next if ($bef eq $key);
				if ($key eq "need" || $key eq "match" || $key eq "subject" || ($in{'match'} && $key eq $match2)) {
					print "<input type=hidden name=\"$key\" value=\"$in{$key}\">\n";
					next;
				}

				$in{$key} =~ s/\0/ /g;
				$in{$key} =~ s/\r\n/<br>/g;
				$in{$key} =~ s/\r/<br>/g;
				$in{$key} =~ s/\n/<br>/g;
				if ($in{$key} =~ /<br>$/) {
					while ($in{$key} =~ /<br>$/) {
						$in{$key} =~ s/<br>$//g;
					}
				}

				$tmp = $cell;
				$tmp =~ s/\$left/$key/;
				$tmp =~ s/\$right/$in{$key}/;

				print "$tmp\n";
				print "<input type=hidden name=\"$key\" value=\"$in{$key}\">\n";

				$bef = $key;
			}
			next;
		}
		if ($flag) {
			$cell .= $_;
			next;
		}

		s/\$script/$script/;

		if (/(<\/body([^>]*)>)/i) {
			$cp_flag=1;
			$tmp = $1;
			s/$tmp/$copy\n$tmp/;
		}

		print;
	}
	close(IN);

	if (!$cp_flag) { print "$copy\n</body></html>\n"; }

	exit;
}

# 時間・ホストを取得
($date,$dat2) = &get_time;
&get_host;

# コマンドタグで件名指定あり
if ($in{'subject'}) {
	$in{'subject'} =~ s/\|/｜/g;
	$in{'subject'} =~ s/;/；/g;
	$subject = $in{'subject'};
}

# ブラウザ情報
$agent = $ENV{'HTTP_USER_AGENT'};
$agent =~ s/<//g;
$agent =~ s/>//g;
$agent =~ s/"//g;
$agent =~ s/&//g;
$agent =~ s/'//g;

# blatj送信
if ($pgType == 2) {
	local($tmpfile,$bef,$param);

	# 一時ファイルを書き出し
	$tmpfile = "./$$\.tmp";
	open(OUT,">$tmpfile") || &error("Write Error: $tmpfile");
	print OUT "────────────────────────────\n";
	print OUT "▼$title送信内容\n";
	print OUT "────────────────────────────\n\n";

	foreach (@key) {
		next if ($_ eq "mode");
		next if ($_ eq "need");
		next if ($_ eq "match");
		next if ($_ eq "subject");
		next if ($in{'match'} && $_ eq $match2);
		next if ($bef eq $_);

		$in{$_} =~ s/\0/ /g;
		$in{$_} =~ s/＜br＞/\n/g;
		$in{$_} =~ s/\.\n/\. \n/g;

		# 添付ファイル拒否
		$in{$_} =~ s/Content-Disposition:\s*attachment;.*//ig;
		$in{$_} =~ s/Content-Transfer-Encoding:.*//ig;
		$in{$_} =~ s/Content-Type:\s*multipart\/mixed;\s*boundary=.*//ig;

		if ($in{$_} =~ /\n/) {
			print OUT "$_ = \n\n$in{$_}\n";
		} else {
			print OUT "$_ = $in{$_}\n";
		}

		$bef = $_;
	}

	print OUT "\n\n";
	print OUT "----------------------------------------------------------------------\n";
	print OUT "Date  : $date\n";
	print OUT "Host  : $host\n";
	print OUT "Agent : $agent\n";
	print OUT "----------------------------------------------------------------------\n";
	close(OUT);

	# パラメータ
	$param = "$mailprog $tmpfile -t $mailto -s \"$subject\"";
	$param .= " -c $in{'email'}" if ($cc_mail && $in{'email'});

	# 送信処理
	open(MAIL,"| $param") || &error("メール送信失敗");
	close(MAIL);

	# 一時ファイル削除
	unlink($tmpfile);

# sendmail送信
} else {
	local($bef,$mbody,$email,$subject2);

	$mbody = <<EOM;
────────────────────────────
▼$title送信内容
────────────────────────────

EOM

	foreach (@key) {
		next if ($_ eq "mode");
		next if ($_ eq "need");
		next if ($_ eq "match");
		next if ($_ eq "subject");
		next if ($in{'match'} && $_ eq $match2);
		next if ($bef eq $_);

		$in{$_} =~ s/\0/ /g;
		$in{$_} =~ s/＜br＞/\n/g;
		$in{$_} =~ s/\.\n/\. \n/g;

		# 添付ファイル拒否
		$in{$_} =~ s/Content-Disposition:\s*attachment;.*//ig;
		$in{$_} =~ s/Content-Transfer-Encoding:.*//ig;
		$in{$_} =~ s/Content-Type:\s*multipart\/mixed;\s*boundary=.*//ig;

		if ($in{$_} =~ /\n/) {
			$mbody .= "$_ = \n\n$in{$_}\n";
		} else {
			$mbody .= "$_ = $in{$_}\n";
		}
		$bef = $_;
	}

	# メールアドレスがない場合は送信先に置き換え
	if ($in{'email'} eq "") { $email = $mailto; }
	else { $email = $in{'email'}; }

	# MIMEエンコード
	if (-e $mimew) {
		require $mimew;
		$subject2 = &mimeencode($subject);

		if ($in{'name'}) {
			$from = &mimeencode("From: \"$in{'name'}\" <$email>");
		} else {
			$from = "From: $email";
		}
	} else {
		$subject2 = &base64($subject);

		if ($in{'name'}) {
			$from = "From: " . &base64("\"$in{'name'}\"") . " <$email>";
		} else {
			$from = "From: $email";
		}
	}

	# sendmail起動
	open(MAIL,"| $mailprog -t -i") || &error("メール送信失敗");
	print MAIL "To: $mailto\n";
	print MAIL $from, "\n";
	print MAIL "Cc: $email\n" if ($cc_mail && $email);
	print MAIL "Subject: $subject2\n";
	print MAIL "MIME-Version: 1.0\n";
	print MAIL "Content-type: text/plain; charset=ISO-2022-JP\n";
	print MAIL "Content-Transfer-Encoding: 7bit\n";
	print MAIL "Date: $dat2\n";
	print MAIL "X-Mailer: $ver\n\n";
	foreach ( split(/\n/, $mbody) ) {
		&jcode'convert(*_, 'jis' ,'sjis');
		print MAIL $_, "\n";
	}
	print MAIL "\n\n";
	print MAIL "----------------------------------------------------------------------\n";
	print MAIL "Date  : $date\n";
	print MAIL "Host  : $host\n";
	print MAIL "Agent : $agent\n";
	print MAIL "----------------------------------------------------------------------\n";
	close(MAIL);
}

# リロード
if ($reload) {
	if ($ENV{'PERLXS'} eq "PerlIS") {
		print "HTTP/1.0 302 Temporary Redirection\r\n";
		print "Content-type: text/html\n";
	}
	print "Location: $back\n\n";
	exit;

# 完了メッセージ
} else {

	local($cp_flag,$tmp);
	open(IN,"$tmp_thx") || &error("Open Error: $tmp_thx");
	print "Content-type: text/html\n\n";
	while (<IN>) {
		s/\$back/$back/;

		if (/(<\/body([^>]*)>)/i) {
			$cp_flag=1;
			$tmp = $1;
			s/$tmp/$copy\n$tmp/;
		}

		print;
	}
	close(IN);

	if (!$cp_flag) { print "$copy\n</body></html>\n"; }

	exit;
}

#-------------------------------------------------
#  入力チェック
#-------------------------------------------------
sub err_check {
	local($f, $bef, $err);

	local($cp_flag, $flag, $cell, $tmp);
	open(IN,"$tmp_err2") || &error("Open Error: $tmp_err2");
	print "Content-type: text/html\n\n";
	while (<IN>) {
		if (/<!-- cell_begin -->/) {
			$flag = 1;
		}
		if (/<!-- cell_end -->/) {
			$flag = 0;

			local($key, $bef, $tmp);

			foreach $key (@key) {
				next if ($key eq "need");
				next if ($key eq "subject");
				next if ($key eq "match");
				next if ($in{'match'} && $key eq $match2);
				next if ($_ eq "match");
				next if ($bef eq $key);

				$tmp = $cell;
				$tmp =~ s/\$left/$key/;

				$f = 0;
				foreach $err (@err) {
					if ($err eq $key) { $f++; last; }
				}
				if ($f) {
					$tmp =~ s|\$right|<span style="color:$alm_col">$keyは入力必須です</span>|;
				} elsif (defined($err{$key})) {
					$tmp =~ s|\$right|<span style="color:$alm_col">$keyの入力内容が大きすぎます</span>|;
				} else {
					$in{$key} =~ s/\r\n/<br>/g;
					$in{$key} =~ s/\r/<br>/g;
					$in{$key} =~ s/\n/<br>/g;
					$in{$key} =~ s/\0/ /g;

					$tmp =~ s/\$right/$in{$key}/;
				}

				print "$tmp\n";
				print "<input type=hidden name=\"$key\" value=\"$in{$key}\">\n";

				$bef = $key;
			}
		}
		if ($flag) {
			$cell .= $_;
			next;
		}

		if (/(<\/body([^>]*)>)/i) {
			$cp_flag = 1;
			$tmp = $1;
			s/$tmp/$copy\n$tmp/;
		}

		print;
	}
	close(IN);

	if (!$cp_flag) { print "$copy\n</body></html>\n"; }

	exit;
}

#-------------------------------------------------
#  フォームデコード
#-------------------------------------------------
sub decode {
	local($buf);
	if ($ENV{'REQUEST_METHOD'} eq "POST") {
		$postflag = 1;
		read(STDIN, $buf, $ENV{'CONTENT_LENGTH'});
	} else {
		$postflag = 0;
		$buf = $ENV{'QUERY_STRING'};
	}

	undef(%in); undef(%err);
	@key = (); @need = (); @err = ();
	$check = 0; $max_flg = 0;
	foreach ( split(/&/, $buf) ) {
		local($key, $val) = split(/=/);
		$key =~ tr/+/ /;
		$key =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;
		$val =~ tr/+/ /;
		$val =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("H2", $1)/eg;

		&jcode'convert(*key, 'sjis');
		&jcode'convert(*val, 'sjis');

		# タグ排除
		$key =~ s/&/＆/g;
		$key =~ s/"/”/g;
		$key =~ s/</＜/g;
		$key =~ s/>/＞/g;
		$key =~ s/'/’/g;
		$val =~ s/&/＆/g;
		$val =~ s/"/”/g;
		$val =~ s/</＜/g;
		$val =~ s/>/＞/g;
		$val =~ s/'/’/g;

		if (length($key) > $max_field || length($val) > $max_field) {
			$max_flg = 1;
			$err{$key} = $val;
		}

		# 必須入力項目
		if ($key =~ /^_(.+)/) {
			$key = $1;
			push(@need,$key);

			if ($val eq "") { $check++; push(@err,$key); }
		}

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;

		push(@key,$key);
	}

	# 返り値
	if ($buf) { return (1); } else { return (0); }
}

#-------------------------------------------------
#  エラー処理
#-------------------------------------------------
sub error {
	unlink($tmpfile) if (-e $tmpfile && $pgType == 2);

	print "Content-type: text/html\n\n";
	open(IN,"$tmp_err1");
	while (<IN>) {
		s/\$error/$_[0]/;

		print;
	}
	close(IN);

	exit;
}

#-------------------------------------------------
#  時間取得
#-------------------------------------------------
sub get_time {
	local($d1,$d2,@w,@m);

	$ENV{'TZ'} = "JST-9";
	local($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');

	# 日時のフォーマット
	$d1 = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);
	$d2 = sprintf("%s, %02d %s %04d %02d:%02d:%02d",
			$w[$wday],$mday,$m[$mon],$year+1900,$hour,$min,$sec) . " +0900";

	return ($d1,$d2);
}

#-------------------------------------------------
#  ホスト名取得
#-------------------------------------------------
sub get_host {
	$host = $ENV{'REMOTE_HOST'};
	$addr = $ENV{'REMOTE_ADDR'};

	if ($gethostbyaddr && ($host eq "" || $host eq $addr)) {
		$host = gethostbyaddr(pack("C4", split(/\./, $addr)), 2);
	}
	if ($host eq "") { $host = $addr; }
}

#-------------------------------------------------
#  チェックモード
#-------------------------------------------------
sub check {
	print "Content-type: text/html\n\n";
	print <<EOM;
<html><head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>チェックモード</title></head>
<body>
<h3>チェックモード</h3>
<ul>
EOM

	# メールソフトチェック
	print "<li>メールソ\フトパス：";
	if (-e $mailprog) {
		print "OK\n";
	} else {
		print "NG → $mailprog\n";
	}

	# jcode.pl バージョンチェック
	print "<li>jcode.plバージョンチェック：";

	if ($jcode'version < 2.13) {
		print "バージョンが低いようです。→ v$jcode'version\n";
	} else {
		print "バージョンOK (v$jcode'version)\n";
	}

	# テンプレート
	foreach ( $tmp_conf, $tmp_err1, $tmp_err2, $tmp_thx ) {
		print "<li>テンプレート ( $_ ) ：";
		if (-e $_) {
			print "パスOK!\n";
		} else {
			print "パスNG → $_\n";
		}
	}

	print <<EOM;
<li>バージョン : $ver
</ul>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  BASE64変換
#-------------------------------------------------
#	とほほのWWW入門で公開されているルーチンを参考にしました。
#	http://tohoho.wakusei.ne.jp/
sub base64 {
	local($sub) = @_;
	&jcode'convert(*sub, 'jis', 'sjis');

	$sub =~ s/\x1b\x28\x42/\x1b\x28\x4a/g;
	$sub = "=?iso-2022-jp?B?" . &b64enc($sub) . "?=";
	$sub;
}
sub b64enc {
	local($ch) = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
	local($x, $y, $z, $i);
	$x = unpack("B*", $_[0]);
	for ($i=0; $y=substr($x,$i,6); $i+=6) {
		$z .= substr($ch, ord(pack("B*", "00" . $y)), 1);
		if (length($y) == 2) {
			$z .= "==";
		} elsif (length($y) == 4) {
			$z .= "=";
		}
	}
	$z;
}

__END__

