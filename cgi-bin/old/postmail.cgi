#!/usr/bin/perl

#��������������������������������������������������������������������
#�� POST-MAIL v3.41 (2006/03/23)
#�� copyright (c) KentWeb
#�� webmaster@kent-web.com
#�� http://www.kent-web.com/
#��������������������������������������������������������������������
$ver = 'postmail v3.41';
#��������������������������������������������������������������������
#�� [���ӎ���]
#�� 1. ���̃X�N���v�g�̓t���[�\�t�g�ł��B���̃X�N���v�g���g�p����
#��    �����Ȃ鑹�Q�ɑ΂��č�҂͈�؂̐ӔC�𕉂��܂���B
#�� 2. ���M�t�H�[����HTML�y�[�W�̍쐬�Ɋւ��ẮAHTML���@�̔��e
#��    �ƂȂ邽�߁A�T�|�[�g�ΏۊO�ƂȂ�܂��B
#�� 3. �ݒu�Ɋւ��鎿��̓T�|�[�g�f���ɂ��肢�������܂��B
#��    ���ڃ��[���ɂ�鎿��͂��󂯂������Ă���܂���B
#��������������������������������������������������������������������
#
# [ ���M�t�H�[�� (HTML) �̋L�q�� ]
#
# �E�^�O�̋L�q�� (1)
#   ���Ȃ܂� <input type=text name="name" size=25>
#   �� ���̃t�H�[���Ɂu�R�c���Y�v�Ɠ��͂��đ��M����ƁA
#      �uname = �R�c���Y�v�Ƃ����`���Ŏ�M���܂�
#
# �E�^�O�̋L�q�� (2)
#   ���D���ȐF <input type=radio name="color" value="��">
#   �� ���̃��W�I�{�b�N�X�Ƀ`�F�b�N���đ��M����ƁA
#      �ucolor = �v�Ƃ����`���Ŏ�M���܂�
#
# �E�^�O�̋L�q�� (3)
#   E-mail <input type=text name="email" size=25>
#   �� name�l�Ɂuemail�v�Ƃ����������g���Ƃ���̓��[���A�h���X
#      �ƔF�����A�A�h���X�̏������ȈՃ`�F�b�N���܂�
#   �� (��) abc@xxx.co.jp
#   �� (�~) abc.xxx.co.jp �� ���̓G���[�ƂȂ�܂�
#
# �E�^�O�̋L�q�� (4)
#   E-mail <input type=text name="_email" size=25>
#   �� name�l�̐擪�Ɂu�A���_�[�o�[ �v��t����ƁA���̓��͒l��
#     �u���͕K�{�v�ƂȂ�܂��B
#      ��L�̗�ł́A�u���[���A�h���X�͓��͕K�{�v�ƂȂ�܂��B
#
# �Ename�l�ւ́u�S�p�����v�̎g�p�͉\�ł�
#  (��) <input type=radio name="�N��" value="20�Α�">
#  �� ��L�̃��W�I�{�b�N�X�Ƀ`�F�b�N�����đ��M����ƁA
#     �u�N�� = 20�Α�v�Ƃ��������Ŏ󂯎�邱�Ƃ��ł��܂��B
#
# �Emimew.pl�g�p���Aname�l���uname�v�Ƃ���Ƃ�����u���M�Җ��v�ƔF��
#   ���đ��M���̃��[���A�h���X���u���M�� <���[���A�h���X>�v�Ƃ���
#   �t�H�[�}�b�g�Ɏ����ϊ����܂��B
#  (�t�H�[���L�q��)  <input type=text name="name">
#  (���M���A�h���X)  ���Y <taro@email.xx.jp>
#
# �E�R�}���h�^�O (1)
#   �� ���͕K�{���ڂ������w�肷��i���p�X�y�[�X�ŕ����w��j
#   �� ���W�I�{�^���A�`�F�b�N�{�b�N�X�΍�
#   �� name�l���uneed�v�Avalue�l���u�K�{����1 + ���p�X�y�[�X +�K�{����2 + ���p�X�y�[�X ...�v
#   (��) <input type=hidden name="need" value="���O ���[���A�h���X ����">
#
# �E�R�}���h�^�O (2)
#   �� 2�̓��͓��e�����ꂩ���`�F�b�N����
#   �� name�l���umatch�v�Avalue�l���u����1 + ���p�X�y�[�X + ����2�v
#   (��) <input type=hidden name="match" value="email email2">
#
# �E�R�}���h�^�O (3)
#   �� ���[���������w�肷��
#   �� ���̏ꍇ�A�ݒ�Ŏw�肷�� $subject ���D�悳��܂��B
#   (��) <input type=hidden name="subject" value="���[���^�C�g������">
#
#  [ �ȈՃ`�F�b�N ]
#   http://�`�`/postmail.cgi?mode=check
#
#  [ �ݒu�� ]
#
#  public_html / index.html (�g�b�v�y�[�W���j
#       |
#       +-- postmail / postmail.cgi  [705]
#                      jcode.pl      [604]
#                      mimew.pl      [604] ... �C��
#                      postmail.html
#                      tmp_*.html ... �e���v���[�g�t�@�C��

#-------------------------------------------------
#  ����{�ݒ�
#-------------------------------------------------

# �����R�[�h�ϊ����C�u����
require './jcode.pl';

# MIME�G���R�[�h���C�u�������g���ꍇ�i�����j
#  �� ���[���w�b�_�̑S�p������BASE64�ϊ�����@�\
#  �� mimew.pl���w��
$mimew = './mimew.pl';

# ���[���\�t�g�܂ł̃p�X
#  �� sendmail�̗� �F/usr/lib/sendmail
#  �� BlatJ�̗�    �Fc:\blatj\blatj.exe
$mailprog = '/usr/sbin/sendmail';

# ���M�惁�[���A�h���X
$mailto = 'kayakclubgoodlife@gmail.com';

# ���̓t�B�[���h������̍ő�e�ʁi�o�C�g�j
# ���Q�l : �S�p1���� = 2�o�C�g
$max_field = 800;

# ���M�O�m�F
#  0 : no
#  1 : yes
$preview = 0;

# ���[���^�C�g��
$subject = '�t�H�[�����[��';

# �{�̃v���O����URL
$script = './postmail.cgi';

# �m�F��ʃe���v���[�g
$tmp_conf = './tmp_conf.html';

# ��ʃG���[��ʃe���v���[�g
$tmp_err1 = './tmp_err1.html';

# ���̓G���[��ʃe���v���[�g
$tmp_err2 = './tmp_err2.html';

# ���M���ʃe���v���[�g
$tmp_thx = './tmp_thx.html';

# ���M��̌`��
#  0 : �������b�Z�[�W���o��.
#  1 : �߂�� ($back) �֎����W�����v������.
$reload = 1;

# ���M��̖߂��
#  �� http://����L�q����
$back = 'http://www.go-goodlife.com/thx.html';

# ���M�� method=POST ���� (0=no 1=yes)
#  �� �Z�L�����e�B�΍�
$postonly = 1;

# �A���[���F
$alm_col = "#dd0000";

# �z�X�g�擾���@
# 0 : gethostbyaddr�֐����g��Ȃ�
# 1 : gethostbyaddr�֐����g��
$gethostbyaddr = 0;

# ���M���֍T�� (CC) �𑗂�
# 0=no 1=yes
# ���Z�L�����e�B�ケ�̋@�\�͐������܂���.
# ��name="email" �̃t�B�[���h�ւ̓��͂��K�{�ƂȂ�܂�.
$cc_mail = 0;

#-------------------------------------------------
#  ���ݒ芮��
#-------------------------------------------------

# �t�H�[���f�R�[�h
$ret = &decode;

# ��{����
if (!$ret) { &error("�s���ȏ����ł�"); }
elsif ($in{'mode'} eq "check") { &check; }

# POST�`�F�b�N
if ($postonly && !$postflag) { &error("�s���ȃA�N�Z�X�ł�"); }

# �����`�F�b�N
if ($in{'subject'} =~ /\r|\n/) { &error("���[���������s���ł�"); }
$in{'subject'} =~ s/\@/��/g;
$in{'subject'} =~ s/\./�D/g;
$in{'subject'} =~ s/\+/�{/g;
$in{'subject'} =~ s/\-/�|/g;
$in{'subject'} =~ s/\:/�F/g;
$in{'subject'} =~ s/\;/�G/g;
$in{'subject'} =~ s/\|/�b/g;

# ���[���v���O�����̎�ރ`�F�b�N
if ($mailprog =~ /blat/i) { $pgType = 2; } else { $pgType = 1; }

# ���쌠�\�L�i�폜�s�j
$copy = <<EOM;
<br><br><div align="center">
<span style="font-size:10px;font-family:Verdana,Helvetica,Arial;">
- <a href="http://www.kou-s.co.jp/" target="_top"></a> -
</span></div>
EOM

# �K�{���̓`�F�b�N
if ($in{'need'}) {
	local(@tmp, @uniq, %seen);

	# need�t�B�[���h�̒l��K�{�z��ɉ�����
	@tmp = split(/\s+/, $in{'need'});
	push(@need,@tmp);

	# �K�{�z��̏d���v�f��r������
	foreach (@need) {
		push(@uniq,$_) unless $seen{$_}++;
	}

	# �K�{���ڂ̓��͒l���`�F�b�N����
	foreach (@uniq) {

		# �t�B�[���h�̒l���������Ă��Ȃ����́i���W�I�{�^�����j
		if (!defined($in{$_})) {
			$check++;
			push(@key,$_);
			push(@err,$_);

		# ���͂Ȃ��̏ꍇ
		} elsif ($in{$_} eq "") {
			$check++;
			push(@err,$_);
		}
	}
}

# ���͓��e�}�b�`
if ($in{'match'}) {
	($match1,$match2) = split(/\s+/, $in{'match'}, 2);

	if ($in{$match1} ne $in{$match2}) {
		&error("$match1��$match2�̍ē��͓��e���قȂ�܂�");
	}
}

# ���̓`�F�b�N�m�F���
if ($check || $max_flg) { &err_check; }

# E-Mail�����`�F�b�N
if ($in{'email'} =~ /\,/) {
	&error("���[���A�h���X�ɃR���} ( , ) ���܂܂�Ă��܂�");
}
if ($in{'email'} && $in{'email'} !~ /^[\w\.\-]+\@[\w\.\-]+\.[a-zA-Z]{2,6}$/) {
	&error("���[���A�h���X�̏������s���ł�");
}

# �v���r���[
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

# ���ԁE�z�X�g���擾
($date,$dat2) = &get_time;
&get_host;

# �R�}���h�^�O�Ō����w�肠��
if ($in{'subject'}) {
	$in{'subject'} =~ s/\|/�b/g;
	$in{'subject'} =~ s/;/�G/g;
	$subject = $in{'subject'};
}

# �u���E�U���
$agent = $ENV{'HTTP_USER_AGENT'};
$agent =~ s/<//g;
$agent =~ s/>//g;
$agent =~ s/"//g;
$agent =~ s/&//g;
$agent =~ s/'//g;

# blatj���M
if ($pgType == 2) {
	local($tmpfile,$bef,$param);

	# �ꎞ�t�@�C���������o��
	$tmpfile = "./$$\.tmp";
	open(OUT,">$tmpfile") || &error("Write Error: $tmpfile");
	print OUT "��������������������������������������������������������\n";
	print OUT "��$title���M���e\n";
	print OUT "��������������������������������������������������������\n\n";

	foreach (@key) {
		next if ($_ eq "mode");
		next if ($_ eq "need");
		next if ($_ eq "match");
		next if ($_ eq "subject");
		next if ($in{'match'} && $_ eq $match2);
		next if ($bef eq $_);

		$in{$_} =~ s/\0/ /g;
		$in{$_} =~ s/��br��/\n/g;
		$in{$_} =~ s/\.\n/\. \n/g;

		# �Y�t�t�@�C������
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

	# �p�����[�^
	$param = "$mailprog $tmpfile -t $mailto -s \"$subject\"";
	$param .= " -c $in{'email'}" if ($cc_mail && $in{'email'});

	# ���M����
	open(MAIL,"| $param") || &error("���[�����M���s");
	close(MAIL);

	# �ꎞ�t�@�C���폜
	unlink($tmpfile);

# sendmail���M
} else {
	local($bef,$mbody,$email,$subject2);

	$mbody = <<EOM;
��������������������������������������������������������
��$title���M���e
��������������������������������������������������������

EOM

	foreach (@key) {
		next if ($_ eq "mode");
		next if ($_ eq "need");
		next if ($_ eq "match");
		next if ($_ eq "subject");
		next if ($in{'match'} && $_ eq $match2);
		next if ($bef eq $_);

		$in{$_} =~ s/\0/ /g;
		$in{$_} =~ s/��br��/\n/g;
		$in{$_} =~ s/\.\n/\. \n/g;

		# �Y�t�t�@�C������
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

	# ���[���A�h���X���Ȃ��ꍇ�͑��M��ɒu������
	if ($in{'email'} eq "") { $email = $mailto; }
	else { $email = $in{'email'}; }

	# MIME�G���R�[�h
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

	# sendmail�N��
	open(MAIL,"| $mailprog -t -i") || &error("���[�����M���s");
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

# �����[�h
if ($reload) {
	if ($ENV{'PERLXS'} eq "PerlIS") {
		print "HTTP/1.0 302 Temporary Redirection\r\n";
		print "Content-type: text/html\n";
	}
	print "Location: $back\n\n";
	exit;

# �������b�Z�[�W
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
#  ���̓`�F�b�N
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
					$tmp =~ s|\$right|<span style="color:$alm_col">$key�͓��͕K�{�ł�</span>|;
				} elsif (defined($err{$key})) {
					$tmp =~ s|\$right|<span style="color:$alm_col">$key�̓��͓��e���傫�����܂�</span>|;
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
#  �t�H�[���f�R�[�h
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

		# �^�O�r��
		$key =~ s/&/��/g;
		$key =~ s/"/�h/g;
		$key =~ s/</��/g;
		$key =~ s/>/��/g;
		$key =~ s/'/�f/g;
		$val =~ s/&/��/g;
		$val =~ s/"/�h/g;
		$val =~ s/</��/g;
		$val =~ s/>/��/g;
		$val =~ s/'/�f/g;

		if (length($key) > $max_field || length($val) > $max_field) {
			$max_flg = 1;
			$err{$key} = $val;
		}

		# �K�{���͍���
		if ($key =~ /^_(.+)/) {
			$key = $1;
			push(@need,$key);

			if ($val eq "") { $check++; push(@err,$key); }
		}

		$in{$key} .= "\0" if (defined($in{$key}));
		$in{$key} .= $val;

		push(@key,$key);
	}

	# �Ԃ�l
	if ($buf) { return (1); } else { return (0); }
}

#-------------------------------------------------
#  �G���[����
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
#  ���Ԏ擾
#-------------------------------------------------
sub get_time {
	local($d1,$d2,@w,@m);

	$ENV{'TZ'} = "JST-9";
	local($sec,$min,$hour,$mday,$mon,$year,$wday) = localtime(time);
	@w = ('Sun','Mon','Tue','Wed','Thu','Fri','Sat');
	@m = ('Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec');

	# �����̃t�H�[�}�b�g
	$d1 = sprintf("%04d/%02d/%02d(%s) %02d:%02d",
			$year+1900,$mon+1,$mday,$w[$wday],$hour,$min);
	$d2 = sprintf("%s, %02d %s %04d %02d:%02d:%02d",
			$w[$wday],$mday,$m[$mon],$year+1900,$hour,$min,$sec) . " +0900";

	return ($d1,$d2);
}

#-------------------------------------------------
#  �z�X�g���擾
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
#  �`�F�b�N���[�h
#-------------------------------------------------
sub check {
	print "Content-type: text/html\n\n";
	print <<EOM;
<html><head>
<META HTTP-EQUIV="Content-type" CONTENT="text/html; charset=Shift_JIS">
<title>�`�F�b�N���[�h</title></head>
<body>
<h3>�`�F�b�N���[�h</h3>
<ul>
EOM

	# ���[���\�t�g�`�F�b�N
	print "<li>���[���\\�t�g�p�X�F";
	if (-e $mailprog) {
		print "OK\n";
	} else {
		print "NG �� $mailprog\n";
	}

	# jcode.pl �o�[�W�����`�F�b�N
	print "<li>jcode.pl�o�[�W�����`�F�b�N�F";

	if ($jcode'version < 2.13) {
		print "�o�[�W�������Ⴂ�悤�ł��B�� v$jcode'version\n";
	} else {
		print "�o�[�W����OK (v$jcode'version)\n";
	}

	# �e���v���[�g
	foreach ( $tmp_conf, $tmp_err1, $tmp_err2, $tmp_thx ) {
		print "<li>�e���v���[�g ( $_ ) �F";
		if (-e $_) {
			print "�p�XOK!\n";
		} else {
			print "�p�XNG �� $_\n";
		}
	}

	print <<EOM;
<li>�o�[�W���� : $ver
</ul>
</body>
</html>
EOM
	exit;
}

#-------------------------------------------------
#  BASE64�ϊ�
#-------------------------------------------------
#	�Ƃقق�WWW����Ō��J����Ă��郋�[�`�����Q�l�ɂ��܂����B
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

