<?php

namespace App\Console\Commands;

use Illuminate\Console\Command;
use Illuminate\Support\Facades\DB;

class AliveDatabaseConnection extends Command
{
    /**
     * The name and signature of the console command.
     *
     * @var string
     */
    protected $signature = 'db:alive';

    /**
     * The console command description.
     *
     * @var string
     */
    protected $description = 'Check if the database connection is alive';

    /**
     * Create a new command instance.
     *
     * @return void
     */
    public function __construct()
    {
        parent::__construct();
    }

    /**
     * Execute the console command.
     *
     * @return int
     */
    public function handle()
    {

        try {

            DB::select('SELECT 1');

            return 0;

        } catch (\Exception $exception)
        {
            return 1;
        }

    }