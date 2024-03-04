from timeit import default_timer as timer

 n_total_steps = len(training_loader)
    for epoch in range(num_epochs):
        start = timer()
        for i, (images, labels) in enumerate(training_loader):
            images = images.to(device)
            labels = labels.type(torch.LongTensor)
            labels = labels.to(device)
    
            outputs = model(images)
            loss = criterion(outputs, labels)
    
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
            if (i+1) % 30 == 0:
                print(f'Epoch [{epoch+1}/{num_epochs}], Step [{i+1}/{n_total_steps}], Loss: {loss.item():.4f}')
        end = timer()
        print(f'Time for Epoch {epoch+1}: {end-start:.4f} seconds')
    
    print('Training Finished')


#evaluation
sample_limit = int(testing_dataset.__len__() / 46)
with torch.no_grad():
    n_correct = 0
    n_samples = 0
    n_class_correct = [0 for i in range(46)]
    n_class_samples = [0 for i in range(46)]
    for images, labels in testing_loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)

        _, predicted = torch.max(outputs, 1)
        n_samples += labels.size(0)
        n_correct += (predicted == labels).sum().item()

        test_limit = min(batch_size, sample_limit)

        for i in range(test_limit):
            label = labels[i]
            pred = predicted[i]
            label = int(label)
            if (label == pred):
                n_class_correct[label] += 1
            n_class_samples[label] += 1

    acc = 100.0 * n_correct / n_samples
    print(f'Accurracy of the network: {acc}%')