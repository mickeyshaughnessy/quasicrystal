program scart
        implicit real*8(a-h,o-z)
        dimension nprim(1000),freal(1000),fimag(1000)
        dimension kpoint(100),npsht(1000,500),nprimh(5000)

        open(8,file='prime',status='unknown',form='formatted')
        open(9,file='cosida',status='unknown',form='formatted')
c
c  this program feeds kpoint in unit of 2*pi/a'
c  calculate cos(k*nprim) and sine(k*nprim)
c
        read(8,100)(nprimh(i),i=1,61)
  100   format(5x,10i10/(5x,10i10))
        do 77 ipr = 1,61
        nprim(ipr) = nprimh(ipr)
  77    continue
        write(9,100)(nprim(i),i=1,61)
c
c  shift the prime numbers to the average
c  the cos ans sin are calculated roughly symmetric
c
        pi = 3.14159
        twopi = 2*pi

        idsum = 0
        limsi = 61
        lacli = 53
        do 1 isum = 1,limsi
        idsum = idsum + nprim(isum)
  1     continue
        nshift = idsum/limsi
        do 6 imovc = 1,3
        if(imovc.eq.0) then
        nmovd = 0
        else
        nmovd = nprimh(imovc)
        endif
        mshitol = nshift + nmovd
        do 4 ish = 1,lacli
        npsht(ish,imovc) = nprim(ish) - nshift
  4     continue
        do 5 ish = 1,lacli
        nprim(ish) = npsht(ish,imovc)
  5     continue
        write(9,104)idsum,imove,nshift,nmovd,mshitol
 104    format(1x,'6 idsum,imoven,shift,nmovd,mshitol',2x,5i10)
        write(9,102)(npsht(ish,imovc),ish=1,50)
 102    format(5x,10i10/(5x,10i10))
c
c  do the scattering
c

       do 2  ik = 1,20
       gk = twopi*ik*0.1
       sumco = 0.d0
       sumim = 0.0d0
       summag = 0.0d0       do 3 ipo = 1,lacli
       pprim = nprim(ipo)
       phase = gk*pprim
       sumco = sumco + dcos(phase)
       sumsi = sumsi + dsin(phase)
       if(ipo.le.5) then
       write(9,103)nprim(ipo),phase,sumco,sumsi
  103  format(1x,'nprim,phase,sumco,sumsi',2x,i10,3f15.5)
       endif
       sumcosq = sumco**2
       sumsisq = sumsi**2
       sumcosi = sumcosq + sumsisq
       summag = summag + dsqrt(sumcosi)
   3   continue
       write(9,101)ik,gk,sumco,sumsi,summag
  101  format(1x,'k,gk,sumco,sumsi,summag',2x,i10,4f12.5)
   2   continue
   6   continue
       stop
       end
