package My::AhoCorasick;
use strict;
use warnings;
use Scalar::Util qw(weaken isweak);

sub new {
    my $class = shift;
    my $self = bless {}, $class;

    $self->{root} = {};
    $self->add_string($_) foreach @_;
    $self->make_failure_links;
    $self;
}

sub add_string {
    my ($self, $string) = @_;

    my @chars = split //, $string;
    my $node = $self->{root};
    $node = ($node->{$_} ||= {}) foreach @chars;
    push @{$node->{_accept}}, length $string;
}

sub make_failure_links {
    my $self = shift;
    my $root = $self->{root};

    my @nodes = ();
    foreach (keys %$root) {
        next if /^_./;
        $root->{$_}->{_failure} = $root;
        push @nodes, $root->{$_};
    }

    while (my $node = shift @nodes) {
        foreach (keys %$node) {
            next if /^_./;
            push @nodes, $node->{$_};

            my $f = $node->{_failure};
            $f = $f->{_failure} until $f->{$_} || $f == $root;
            $node->{$_}->{_failure} = $f->{$_} || $root;

            weaken $node->{$_}->{_failure} unless isweak $node->{$_}->{_failure};

            if (my $suffixes = $node->{$_}->{_failure}->{_accept}) {
                push @{$node->{$_}->{_accept}}, @$suffixes;
            }
        }
    }
}

sub match {
    my ($self, $string) = @_;
    my $node = my $root = $self->{root};

    my @chars = split //, $string;
    my @found = ();
    foreach my $i (0..$#chars) {
        if (my $next = $node->{$chars[$i]}) {
            $node = $next;
        } else {
            $node = $node->{_failure} until $node->{$chars[$i]} || $node == $root;
            $node = $node->{$chars[$i]} || $root;
        }
        if ($node->{_accept}) {
            push @found, [$i + 1 - $_, $_] foreach @{$node->{_accept}};
        }
    }
    return @found;
}
