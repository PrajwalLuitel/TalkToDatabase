import React from 'react';
import Image from 'next/image';
import { Edu_VIC_WA_NT_Beginner } from "next/font/google";


const edu_font = Edu_VIC_WA_NT_Beginner({
    subsets: ["latin"],
    weight: ["400"],
});
  



const LoadingAnimation = ({message}) => {
  return (
      <div className={`text-center bg-loading-background pt-[9rem] bg-center animate-pulse ${edu_font.className} bg-no-repeat`}>
          <p>{message}</p>
      </div>
  )
}

export default LoadingAnimation