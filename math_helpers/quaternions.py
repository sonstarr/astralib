#!/usr/bin/env python3
import numpy as np
from matrices import *


def prv2dcm(e1, e2, e3, theta):
    """converts a principle rotation vector with an angle to a dcm
    """
    dcm = np.zeros([3,3])
    z = 1.0 - np.cos(theta)
    dcm = [[e1*e1*z+np.cos(theta), e1*e2*z+e3*np.sin(theta), e1*e3*z-e2*np.sin(theta)],
           [e2*e1*z-e3*np.sin(theta), e2*e2*z+np.cos(theta), e2*e3*z+e1*np.sin(theta)],
           [e3*e1*z+e2*np.sin(theta), e3*e2*z-e1*np.sin(theta), e3*e3*z+np.cos(theta)]]
    return dcm

def prv_angle(dcm):
    """compute the principle rotation angle from a dcm
    """
    theta = np.arccos(1./2. * (dcm[0][0] + dcm[1][1] + dcm[2][2] - 1))
    return theta


def prv_axis(dcm):
    """compute the principle rotation vector from a dcm
    """
    theta = prv_angle(dcm)
    factor = 1./(2.*np.sin(theta))
    e1 = factor * (dcm[1][2] - dcm[2][1])
    e2 = factor *(dcm[2][0] - dcm[0][2])
    e3 = factor *(dcm[0][1] - dcm[1][0])
    return e1, e2, e3

    
def quat2dcm(s1, q1, q2, q3):
    """converts a quaternion set into a dcm
    """
    dcm = np.zeros([3,3])
    dcm = [[s1*s1+q1*q1-q2*q2-q3*q3, 2*(q1*q2+s1*q3), 2*(q1*q3-s1*q2)],
           [2*(q1*q2-s1*q3), s1*s1-q1*q1+q2*q2-q3*q3, 2*(q2*q3+s1*q1)],
           [2*(q1*q3+s1*q2), 2*(q2*q3-s1*q1), s1*s1-q1*q1-q2*q2+q3*q3]]
    return dcm


def dcm2quat(dcm):
    """converts a dcm into a quaternion set
    """
    trace = dcm[0][0] + dcm[1][1] + dcm[2][2]
    s1 = 1./2. * np.sqrt(trace + 1)
    b1 = (dcm[1][2]-dcm[2][1]) / (4*s1)
    b2 = (dcm[2][0]-dcm[0][2]) / (4*s1)
    b3 = (dcm[0][1]-dcm[1][0]) / (4*s1)


def dcm2quat_sheppard(dcm):
    """converts a dcm to quaternions based on sheppard's method;
    see pg 110, Analytical Mechanics of Space Systems
    """
    trace = dcm[0][0] + dcm[1][1] + dcm[2][2]
    s1_sq = 1./4. * (1+trace)
    b1_sq = 1./4. * (1+2*dcm[0][0]-trace)
    b2_sq = 1./4. * (1+2*dcm[1][1]-trace)
    b3_sq = 1./4. * (1+2*dcm[2][2]-trace)
    quats = [s1_sq, b1_sq, b2_sq, b3_sq]
    print(quats)
    if np.argmax(quats) == 0:
        s1 = np.sqrt(s1_sq)
        b1 = (dcm[1][2]-dcm[2][1])/(4.*s1)
        b2 = (dcm[2][0]-dcm[0][2])/(4.*s1)
        b3 = (dcm[0][1]-dcm[1][0])/(4.*s1)
    elif np.argmax(quats) == 1:
        b1 = np.sqrt(b1_sq)
        s1 = (dcm[1][2]-dcm[2][1])/(4.*b1)
        b2 = (dcm[0][1]+dcm[1][0])/(4.*b1)
        b3 = (dcm[2][0]+dcm[0][2])/(4.*b1)
    elif np.argmax(quats) == 2:
        b2 = np.sqrt(b2_sq)
        s1 = (dcm[2][0]-dcm[0][2])/(4.*b2)
        b1 = (dcm[0][1]+dcm[1][0])/(4.*b2)
        b3 = (dcm[1][2]+dcm[2][1])/(4.*b2)
    elif np.argmax(quats) == 3:
        b3 = np.sqrt(b3_sq)
        s1 = (dcm[0][1]-dcm[1][0])/(4.*b3)
        b1 = (dcm[2][0]+dcm[0][2])/(4.*b3)
        b2 = (dcm[1][2]+dcm[2][1])/(4.*b3)
    return [s1, b1, b2, b3]


def euler2quat(a1, a2, a3, sequence='313'):
    """returns quaternion set from an euler sequence, currently only
    accepts 313 sequence
    """
    if sequence == '313':
        s1 = np.cos(a2/2.) * np.cos((a3+a1)/2.)
        b1 = np.sin(a2/2.) * np.cos((a3-a1)/2.)
        b2 = np.sin(a2/2.) * np.sin((a3-a1)/2.)
        b3 = np.cos(a2/2.) * np.sin((a3+a1)/2.)
    return [s1, b1, b2, b3]



if __name__ == "__main__":
    # testing principle rotation parameters
    # deg = np.deg2rad([10, 25, -15])
    # matrix = rotate_euler(deg[0], deg[1], deg[2], '321')
    # angle = np.rad2deg(prv_angle(matrix))
    # axis = prv_axis(matrix)
    # print(matrix)
    # print(angle)
    # print(axis)
    # print(angle - 360.)

    # testing quaternions
    b1, b2, b3 = np.deg2rad([30, -45, 60])

    brotate = rotate_euler(b1, b2, b3, '321')
        #print(f'BN: {brotate}')

    f1, f2, f3 = np.deg2rad([10., 25., -15.])
    frotate = rotate_euler(f1, f2, f3, '321')
    frot = rotate_sequence(f1, f2, f3, '321')
    print(f'FN: {frotate}')
    quats = dcm2quat_sheppard(frotate)
    print(quats)

    a1, a2, a3 = dcm_inverse(frotate, sequence='313')
    print(np.rad2deg(a1), np.rad2deg(a2), np.rad2deg(a3))
    quat = euler2quat(a1, a2 , a3, sequence='313')
    print(quat)