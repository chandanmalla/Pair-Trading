#!/usr/bin/python

#https://www.kaggle.com/theoviel/fast-fourier-transform-denoising
def filter_signal(signal, threshold=3e4):
    '''
    Function to perform FFT
    
    ======Argument=====
    signal----Dataset
    
    ======Return======
    fourier --- Thresholded or noise free dataset
    '''
    fourier = rfft(signal)
    frequencies = rfftfreq(len(signal), d=20e-3/len(signal))
    fourier[frequencies > threshold] = 0
    return irfft(fourier)




def fft(df,thresh):
    '''
    Function to return FFT data
    
    ======Argument=====
    df----Dataset
    thresh --Threshold to perform FFT
    
    ======Return======
    temp_df_fft --- Thresholded or noise free dataset
    '''
    
    
    columns = list(data_2.columns)
    columns.pop(-1)## Removing 'Y_pred' which is at last position
    
    temp_df = pd.DataFrame()
    size = int(df.shape[0])
    
    for cols in columns: ## Y_Pred column is not used for FFT
        temp_df[cols] = filter_signal(df[cols][0:size],threshold=thresh)
        
    temp_df.index = df[0:size].index
    temp_df_fft = temp_df.copy()
    temp_df_fft['Y_pred'] = df['Y_pred'][0:size]
    
    return temp_df_fft