from flask import Flask ,render_template,url_for,request,Response,redirect,send_file
import pandas as pd

app = Flask(__name__ ,template_folder='templates')

#routes

@app.route('/',methods =['GET','POST'])
def main():
    if request.method == 'GET':
        return render_template('index.html' , webName = "Excel to text generator")

    elif request.method == 'POST':
        file = request.files['file']
        narration = request.form['narration']
        extractFileName = file.filename[:file.filename.find('.')]
        print(extractFileName)
        df = pd.read_excel(file,header=1) # header=1

        Ac_No = []
        Amount = []
        
        #Extracting the data from the file 
        for i in range(0,len(df['SR. NO.'])-1):
            Ac_No.append(str(int(df['A/C NO.'][i])))
            Amount.append(str(int(df['AMOUNT'][i])))
        
        
        # tsc_no = input("Enter the transaction id : ")
        # while(tsc_no>2 and tsc_no == 0):
        #     print("Enter a valid transaction id !!")
        #     tsc_no = int(input("Enter the transaction id : "))
        
        #Storing the constant values
        credit_transaction_id = '01'
        debit_transaction_id = '54'
        debit_accountNumber = "98534501853"
        
        # narration = input("STEP 2 [ENTER NARRATION] : ")
        # while(len(narration)<=0 or len(narration)>50):
        #     print("Enter the valid narration")
        #     narration = input("Enter the Narration : ")
        
        if(len(narration)<50):
            narration += (50 - len(narration)) * " "    
        
        
        #Lists for the encrypted Items
        enc_AcNo = [] 
        enc_Amt = []      
        
        acc_bits = "00000000000000000"  #17bits acc val
        
        #Encrypting the bits for Ac/no [1st Column]
        for j in range(len(Ac_No)):
            newac = acc_bits.removeprefix('0'*len(Ac_No[j]))
            newAcval = newac + Ac_No[j]
            enc_AcNo.append(newAcval)
        
        #Encrypting the bits for Amount [2nd Column]
        amt_bits = "0000000000000000"  #16bits acc val
        for k in range(len(Amount)):
            amt_removedBits = amt_bits.removeprefix('0'*len(Amount[k]))
            new_amtVal = amt_removedBits[:-2] + Amount[k] + amt_removedBits[-2:]
            enc_Amt.append(new_amtVal)
        
        #Encrypting the bits for debit Ac/no [Last Row]  
        totalVal = 0
        debit_acc_bits = "00000000000000000"
        debit_acc_removedBits = debit_acc_bits.removeprefix('0'*len(debit_accountNumber))
        new_debit_acc = debit_acc_removedBits + debit_accountNumber
        
        for m in range(len(Amount)):
            totalVal += int(Amount[m])
        
        str_totalVal = str(totalVal)     
        amt_removedBits = amt_bits.removeprefix('0'*len(str_totalVal))
        new_totalAmt = amt_removedBits[:-2] + str_totalVal + amt_removedBits[-2:]
        
        
        # text_fileName = input("Enter .txt fileName : ")
        f = open(f'{extractFileName}.txt' , 'w')
        for n in range(len(Ac_No)):
            f.write(f'{credit_transaction_id}{enc_AcNo[n]}{enc_Amt[n]}{narration}{" " * 16}\n')
        
        f.write(f'{debit_transaction_id}{new_debit_acc}{new_totalAmt}{narration}{" " * 16}')
        f.close()
    
        textfile = f'{extractFileName}.txt'
        print(textfile)
        
        #convert to csv and download
        return send_file(f"{extractFileName}.txt",as_attachment=True,download_name=f"{extractFileName}.txt") 


if __name__ == "__main__":
    app.run(host='0.0.0.0' , debug=True)