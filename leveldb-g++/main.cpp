#include <cassert>
#include <iostream>
#include <leveldb/db.h>
#include <leveldb/write_batch.h>

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cerr << "./a.out [db path]" << std::endl;
        return -1;
    }
    std::string db_path(argv[1]);
    leveldb::DB* db;
    leveldb::Options options;
    options.create_if_missing = true;
    
    // 1. open database
    leveldb::Status status = leveldb::DB::Open(options, db_path , &db);
    if (!status.ok()) {
        std::cerr << "Can not open database: " << status.ToString() << std::endl;
        return 1;
    }

    // 2. write KV pair
    leveldb::WriteOptions writeOptions;
    status = db->Put(writeOptions, "key1", "Hello");
    assert(status.ok());
    status = db->Put(writeOptions, "key2", "LevelDB");
    assert(status.ok());
    
    // 3. read by key
    leveldb::ReadOptions readOptions;
    std::string value;
    status = db->Get(readOptions, "key1", &value);
    if (status.ok()) {
        std::cout << "value of key1: " << value << std::endl;
    } else {
        std::cerr << "failed to read key1 " << status.ToString() << std::endl;
    }

    // 4. write in batch
    leveldb::WriteBatch batch;
    batch.Put("key3", "Batch");
    batch.Put("key4", "Example");
    status = db->Write(writeOptions, &batch);
    assert(status.ok());

    // 5. iterate the database
    std::cout << "\nAll Content:" << std::endl;
    leveldb::Iterator* it = db->NewIterator(readOptions);
    for (it->SeekToFirst(); it->Valid(); it->Next()) {
        std::cout << it->key().ToString() << ": " 
                  << it->value().ToString() << std::endl;
    }
    delete it;

    // 6. close the database
    delete db;

    return 0;
}
