#!/usr/bin/env perl
use strict;
use warnings;
use utf8;

use Test::More qw(no_plan);
use Path::Class qw(file);
use Encode;

use_ok 'My::AhoCorasick';

{
    my $ac = My::AhoCorasick->new(qw/he hers his she/);
    isa_ok $ac, 'My::AhoCorasick';

    my @result = $ac->match('a his hoge hershe xx.');
    is_deeply(
        \@result,
        [
         [ 2, 3], # his
         [11, 2], # he
         [11, 4], # hers
         [14, 3], # she
         [15, 2], # he
        ]
    );
}


{
    my $keywords = decode_utf8(file('keyword.utf8.uniq.txt')->slurp);
    my @keywords = split /\n/, $keywords;
    my $ac = My::AhoCorasick->new(@keywords);
    my $text = <<__TEXT__;
今日は天気がよかったので、近くの海まで愛犬のしなもんと一緒にお散歩。写真は海辺を楽しそうに歩くしなもん。そのあとついでにお買い物にも行ってきました。「はてなの本」を買ったので、はてなダイアリーの便利な商品紹介ツール「はまぞう」を使って紹介してみるよ。とてもおもしろいのでみんなも読んでみてね。
__TEXT__
    my @result = $ac->match($text);
    is_deeply(
        [ map { substr($text, $_->[0], $_->[1]) } @result ],
        [ qw/今日 天気 しなもん 散歩 写真 海辺 しなもん はてな はてなの本 はてな はてなダイアリ はてなダイアリー ダイアリー 商品 はまぞう おもしろい/ ],
    );
}

