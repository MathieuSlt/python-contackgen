import pytest
from unittest import mock
from src.attacks import ScapyAttack


@pytest.fixture(scope='module')
def scapy_attack():
    # Set up a ScapyAttack object with some example parameters
    return ScapyAttack(ip_source='192.168.0.1', ip_dest='10.0.0.1', duration=5)


def test_smurf_attack(scapy_attack):
    # Patch the scapy send function so that it does not send any packets
    with mock.patch('src.attacks.scapy.send') as mock_send:
        scapy_attack.smurf_attack()
        # Ensure that the send function was called at least once
        assert mock_send.called is True


def test_syn_flooding_attack(scapy_attack):
    # Patch the scapy send function so that it does not send any packets
    with mock.patch('src.attacks.scapy.send') as mock_send:
        scapy_attack.syn_flooding_attack()
        # Ensure that the send function was called at least once
        assert mock_send.called is True


def test_ping_of_death(scapy_attack):
    # Patch the scapy send function so that it does not send any packets
    with mock.patch('src.attacks.scapy.send') as mock_send:
        scapy_attack.ping_of_death()
        # Ensure that the send function was called at least once
        assert mock_send.called is True


def test_execute(scapy_attack):
    # Mock the attack function
    attack_function = mock.Mock()
    # Call execute with a duration of 2 seconds and the mock attack function
    scapy_attack.execute(duration=2, attack_function=attack_function)
    # Ensure that the attack function was called at least once
    assert attack_function.called is True
    # Ensure that the attack function was called more than once
    assert attack_function.call_count > 1


def test_str(scapy_attack):
    # Ensure that the string representation of the ScapyAttack object is correct
    assert str(
        scapy_attack) == "ScapyAttack(ip_source=192.168.0.1, ip_dest=10.0.0.1, duration=5)"
