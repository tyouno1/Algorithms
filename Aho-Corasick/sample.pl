#!/usr/bin/env perl
use strict;
use warnings;

use FindBin::libs;
use Perl6::Say;

use My::AhoCorasick;

my $text = 'a his hoge hershe';
my $ac = My::AhoCorasick->new(qw/he hers his she/);
my @result = $ac->match($text);

for (@result) {
    printf "pos %2d, len %d => %s\n", $_->[0], $_->[1], substr($text, $_->[0], $_->[1]);
}
