import React from 'react'

const Footer = () => {
  return (
      <div className="flex flex-col gap-8 bg-emerald-900/30 p-14 mt-10 text-slate-200 ">
      <div className="flex flex-row justify-center  w-full gap-10 max-md:gap-4 text-center text-lg">
        <div className="flex">
        Aarjeyan Shrestha <br/> C0927422
        </div>
        <div className="flex">
        Prajwal Luitel <br/> C0927658
        </div>
        <div className="flex">
        Rajan Ghimire <br/> C0924991
        </div>
        <div className="flex">
        Sudip Chaudhary <br/> C0922310
        </div>
      </div>

      <div className="flex justify-center gap-8 text-center leading-8 font-semibold text-xl pt-3">
        Artificial Intelligence and Machine Learning
        <br/> Lambton College in Toronto
      </div>
        
      </div>
  )
}

export default Footer