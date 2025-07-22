import os
import pandas as pd
import torch
import time
import numpy as np
import warnings
from gensim.models.word2vec import Word2Vec
from model import BatchProgramCC
from torch.autograd import Variable
from sklearn.metrics import precision_recall_fscore_support

warnings.filterwarnings("ignore")
from tqdm import tqdm


def get_batch(dataset, idx, bs):
    tmp = dataset.iloc[idx : idx + bs]
    x1, x2, labels = [], [], []
    for _, item in tmp.iterrows():
        x1.append(item["func_x"])
        x2.append(item["func_y"])
        labels.append([item["label"]])
    return x1, x2, torch.FloatTensor(labels)


if __name__ == "__main__":
    project_root = "astnn/"
    astnn_dir = os.path.join(project_root, "astnn", "data")
    benchmark_name = "bcb"
    print("Train for ", str.upper(benchmark_name))

    train_data = pd.read_pickle("astnn/data/bcb/train/blocks.pkl")
    test_data = pd.read_pickle("astnn/data/bcb/test/blocks.pkl")

    word2vec = Word2Vec.load("astnn/data/bcb/train/embedding/node_w2v_128").wv
    MAX_TOKENS = word2vec.vectors.shape[0]
    EMBEDDING_DIM = word2vec.vectors.shape[1]
    embeddings = np.zeros((MAX_TOKENS + 1, EMBEDDING_DIM), dtype="float32")
    embeddings[: word2vec.vectors.shape[0]] = word2vec.vectors

    HIDDEN_DIM = 100
    ENCODE_DIM = 128
    LABELS = 1
    EPOCHS = 5
    BATCH_SIZE = 32
    USE_GPU = True if torch.cuda.is_available() else False  # TODO

    model = BatchProgramCC(
        EMBEDDING_DIM, HIDDEN_DIM, MAX_TOKENS + 1, ENCODE_DIM, LABELS, BATCH_SIZE, USE_GPU, embeddings
    )
    model.load_state_dict(torch.load("astnn/data/bcb/astnn_bcb_4"))
    model.eval()
    if USE_GPU:
        model.cuda()
    parameters = model.parameters()
    optimizer = torch.optim.Adamax(parameters)
    loss_function = torch.nn.BCELoss()

    pytorch_total_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(pytorch_total_params)

    precision, recall, f1 = 0, 0, 0
    print("Start training...")
    train_data_t, test_data_t = train_data, test_data

    from datetime import datetime

    # training procedure
    for epoch in range(EPOCHS):
        print(f"Epoch {epoch}/{EPOCHS}...")
        start_time = time.time()
        # training epoch
        total_acc = 0.0
        total_loss = 0.0
        total = 0.0
        i = 0

        while i < len(train_data_t):
            print("training....epoch#", epoch, "batch#", i, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
            batch = get_batch(train_data_t, i, BATCH_SIZE)
            i += BATCH_SIZE
            train1_inputs, train2_inputs, train_labels = batch
            if USE_GPU:
                train1_inputs, train2_inputs, train_labels = train1_inputs, train2_inputs, train_labels.cuda()

            model.zero_grad()
            model.batch_size = len(train_labels)
            model.hidden = model.init_hidden()
            output = model(train1_inputs, train2_inputs)

            loss = loss_function(output, Variable(train_labels))
            loss.backward()
            optimizer.step()

        torch.save(model.state_dict(), f"{astnn_dir}/{benchmark_name}/astnn_{benchmark_name}_{epoch}")

    print("Testing...")
    # testing procedure
    predicts = []
    trues = []
    total_loss = 0.0
    total = 0.0
    i = 0
    while i < len(test_data_t):
        print("testing.... batch#", i, datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        batch = get_batch(test_data_t, i, BATCH_SIZE)
        i += BATCH_SIZE
        test1_inputs, test2_inputs, test_labels = batch
        if USE_GPU:
            test_labels = test_labels.cuda()
        model.batch_size = len(test_labels)
        model.hidden = model.init_hidden()
        output = model(test1_inputs, test2_inputs)
        loss = loss_function(output, Variable(test_labels))
        # calc testing acc
        predicted = (output.data > 0.5).cpu().numpy()
        predicts.extend(predicted)

        trues.extend(test_labels.cpu().numpy())
        total += len(test_labels)
        total_loss += loss.item() * len(test_labels)

    precision, recall, f1, _ = precision_recall_fscore_support(trues, predicts, average="binary")

    # savae results to file
    from datetime import datetime

    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    res = f"{now}: {benchmark_name} Precision: {precision} Recall: {recall} F1: {f1}"
    f = open(f"results_astnn_{benchmark_name}.txt", "a")
    f.write(res)
    f.close()
    print(res)
