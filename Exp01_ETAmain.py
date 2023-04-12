import torch
import torch.nn as nn
from sklearn.preprocessing import StandardScaler
import pandas as pd
import random
from sklearn.metrics import r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from torch.optim.lr_scheduler import ExponentialLR

# 读取数据集
data = pd.read_csv('stop_clean.csv', nrows=500)
data['enter_port_time'] = pd.to_datetime(data['enter_port_time'], format='%Y-%m-%d %H:%M:%S')
data = data.sort_values(by=['enter_port_time'])
X = data[['port_lon', 'port_lat', 'port_id', 'stop_time', 'month', 'season', 'Deadweight', 'Powerkwmax', 'TEU', 'volume']].values
y = data[['enter_port_time']].values

# 缺失值填充
X = pd.DataFrame(X)
X = X.fillna(X.median())

# 准备数据集
scaler = StandardScaler()
X = scaler.fit_transform(X)
y = scaler.fit_transform(y)

train_size = int(0.98 * len(X))

X_train = X[:train_size].reshape(train_size, X.shape[1], x)
X_test = X[train_size:].reshape(X.shape[0]-train_size, X.shape[1], x)

y_train, y_test = y[:train_size], y[train_size:]
y_train = y_train.reshape(-1, 1) 
y_test = y_test.reshape(-1, 1)

train_dataset = torch.utils.data.TensorDataset(torch.tensor(X_train), torch.tensor(y_train))
train_loader = torch.utils.data.DataLoader(train_dataset, batch_size=8, shuffle=True)

test_dataset = torch.utils.data.TensorDataset(torch.tensor(X_test), torch.tensor(y_test))
test_loader = torch.utils.data.DataLoader(test_dataset, batch_size=8, shuffle=False)

# 定义模型
class TransformerModel(nn.Module):
    def __init__(self, input_size, hidden_size, num_layers, dropout):
        super(TransformerModel, self).__init__()
        self.transformer = nn.Transformer(d_model=input_size, nhead=1, num_encoder_layers=num_layers, num_decoder_layers=num_layers, dropout=dropout)
        self.fc = nn.Linear(input_size, hidden_size)
        self.output = nn.Linear(hidden_size, 1)
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, x):
        
        x = x.permute(1, 0, 2)
        transformer_output = self.transformer(x, x)
        transformer_output = transformer_output.permute(1, 0, 2)
        transformer_output = transformer_output.reshape(transformer_output.size(0), -1) 
        x = self.fc(transformer_output)
        x = torch.relu(x)
        x = self.dropout(x)
        x = self.output(x)
        x = x.reshape(-1, x.size(1), 1)
        return x

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = TransformerModel(10, 8, num_layers=2, dropout=0.2).to(device)

# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
scheduler = ExponentialLR(optimizer, gamma=0.9)

# 训练模型
num_epochs = 100
losses = []
for epoch in range(num_epochs):
    for i, (inputs, labels) in enumerate(train_loader):
        optimizer.zero_grad()
        outputs = model(inputs.float())
        labels = labels.float().unsqueeze(1)
        loss = criterion(outputs, labels.float())
        loss.backward()
        optimizer.step()
        scheduler.step()
        losses.append(loss.item()) # 记录loss
 
        if (i+1) % 10 == 0:
            print('Epoch [{}/{}], Step [{}/{}], Loss: {:.4f}'.format(epoch+1, num_epochs, i+1, len(train_loader), loss.item()))

# 绘制loss曲线
plt.plot(losses)
plt.xlabel("Step")
plt.ylabel("Loss")
plt.show()

# 测试模型
model.eval()
with torch.no_grad():
    y_predicted = model(torch.from_numpy(X_test).float().to(device))
    y_predicted = y_predicted.cpu() # 将模型输出从GPU移动到CPU
    test_loss = criterion(y_predicted, torch.from_numpy(y_test).float().to(device))
    r2 = r2_score(y_test, y_predicted.numpy())
    mae = mean_absolute_error(y_test, y_predicted.numpy())
    print('Test Loss: {:.4f}'.format(test_loss.item()))
    print('R-squared: {:.4f}'.format(r2))
    print('Mean Absolute Error: {:.4f}'.format(mae))

# 反归一化处理得到预测结果
y_predicted = scaler.inverse_transform(y_predicted.reshape(-1, 1))

# 计算误差百分比
y_test_denorm = scaler.inverse_transform(y_test.reshape(-1, 1))
error = abs((y_predicted - y_test_denorm) / y_test_denorm)
print('Mean Percentage Error: {:.4f}%'.format(torch.Tensor(error).mean().item() * 100))

# 绘制测试集预测结果与真实结果的对比曲线
plt.plot(y_test_denorm, 'ro', label='True Values')
plt.plot(y_predicted, label='Predictions')
plt.xlabel('Sample')
plt.ylabel('Enter Port Time')
plt.legend()
plt.show()




