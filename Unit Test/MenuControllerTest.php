<?php

namespace Tests\Unit;

use App\Http\Controllers\AdminController;
use App\Http\Controllers\MenuController;
use App\Models\Product;
use App\Models\User;
use Illuminate\Foundation\Testing\DatabaseTransactions;
use Illuminate\Http\Request;
use Illuminate\Http\UploadedFile;
use Illuminate\Support\Facades\Storage;
use Tests\TestCase;

class MenuControllerTest extends TestCase
{
    use DatabaseTransactions;
    protected $cus = 'congdanhabc@outlook.com.vn';
    protected $admin = 'ncongdanh91@gmail.com';
    protected $cartAmount;
    protected function authenticate($email_user)
    {
        $user = User::where('email', $email_user)->first();
        if (!$user) {
            $this->markTestSkipped('User not found for testing.');
        }

        $this->actingAs($user);
        return $user;
    }


    public function test_menu_index()
    {
        // $user = $this->authenticate($this->cus);
        $controller = new MenuController();
        $response = $controller->menu();
        $view_name = $response->name();
        dump("View's name is: ". $view_name);
        $view_data = $response->getData();
        $products_view = $view_data['products'];
        $products_db = Product::all()->toArray();


        $this->assertEquals('menu', $view_name);

        foreach ($products_db as $index => $product_db)
        {
            $product_view = $products_view[$index];
            $this->assertEquals($product_db['id'], $product_view['id'], "Product ID mismatch at index: {$index}");
            $this->assertEquals($product_db['name'], $product_view['name'], "Product Name mismatch at index: {$index}");
            dump("Product ID: " . $product_db['id'] . ", Name: " . $product_db['name'] . " - Check: Pass");
        }
    }

    public function test_admin_menu_index()
    {
        $user = $this->authenticate($this->admin);
        $controller = new AdminController();
        $response = $controller->food_menu();
        $view_name = $response->name();
        dump("View's name is: ". $view_name);
        $view_data = $response->getData();

        //Sử dụng json_encode để mã hóa đối tượng stdClass thành chuỗi JSON.
        //Sau đó sử dụng json_decode để giải mã chuỗi JSON thành mảng, với tham số true để đảm bảo nó trở thành mảng liên kết.
        $products_view = json_decode(json_encode($view_data['products']), true);

        $products_db = Product::all()->toArray();


        $this->assertEquals('admin.menu', $view_name);

        foreach ($products_db as $index => $product_db)
        {
            $product_view = $products_view[$index];
            $this->assertEquals($product_db['id'], $product_view['id'], "Product ID mismatch at index: {$index}");
            $this->assertEquals($product_db['name'], $product_view['name'], "Product Name mismatch at index: {$index}");
            dump("Product ID: " . $product_db['id'] . ", Name: " . $product_db['name'] . " - Check: Pass");
        }
    }


    public function test_menu_add_proces()
    {
        //Prepare Data (including a mock image)
        Storage::fake('public');
        $file = UploadedFile::fake()->image('test_image.jpg');
        $testPrice = 20;
        $data = [
            'name' => 'Test Product',
            'description' => 'Test Description',
            'price' => $testPrice,
            'catagory' => 'regular',
            'session' => 1,
            'available' => 'In Stock',
            'image' => $file,
        ];

        $user = $this->authenticate($this->admin);
        $controller = new AdminController();
        $request = new Request($data);
        $request->files->set('image', $data['image']);
        $response = $controller->menu_add_process($request);

        $this->assertEquals("Menu added successfully !", session('success'));
        $this->assertDatabaseHas('products', [
            'name' => $data['name'],
            'description' => $data['description'],
            'price' => $data['price'],
            'catagory' => $data['catagory'],
            'session' => $data['session'],
            'available' => $data['available'],
        ]);
        dump("test_menu_add_proces: Pass");
    }

    public function test_menu_add_proces_with_negative_price()
    {
        //Prepare Data (including a mock image)
        Storage::fake('public');
        $file = UploadedFile::fake()->image('test_image.jpg');
        $testPrice = -20;
        $data = [
            'name' => 'Test Product',
            'description' => 'Test Description',
            'price' => $testPrice,
            'catagory' => 'regular',
            'session' => 1,
            'available' => 'In Stock',
            'image' => $file,
        ];

        $user = $this->authenticate($this->admin);
        $controller = new AdminController();
        $request = new Request($data);
        $request->files->set('image', $data['image']);
        $response = $controller->menu_add_process($request);

        $this->assertEquals('Negative Price value do not accept !', session('wrong'));
        $this->assertDatabaseMissing('products',['name'=>'Test Product']);
        dump("test_menu_add_proces_with_negative_price: Pass");
    }

    public function test_menu_delete_process()
    {
        $user = $this->authenticate($this->admin);
        $product = Product::find(1);
        dump("Delete product has id: ". $product->id);
        $controller = new AdminController();
        $response = $controller->menu_delete_process($product->id);
        $this->assertEquals('Menu  deleted successfully !', session('success'));
        $this->assertDatabaseMissing('products',['id'=> $product->id]);
        dump("test_menu_delete_process: Pass");
    }

    public function test_menu_edit_process()
    {
        //Prepare Data (including a mock image)
        $product = Product::find(1);
        $testPrice = 999;
        $data = [
            'name' => 'Update Product',
            'description' => 'Update Description',
            'price' => $testPrice,
            'catagory' => $product['catagory'],
            'session' => $product['session'],
            'available' => $product['available'],
            'image' => NULL,
        ];

        $user = $this->authenticate($this->admin);
        $controller = new AdminController();
        $request = new Request($data);
        $response = $controller->menu_edit_process($request, $product['id']);

        $this->assertEquals("Menu updated successfully !", session('success'));
        $this->assertDatabaseHas('products', [
            'id'=> $product['id'],
            'name' => $data['name'],
            'description' => $data['description'],
            'price' => $data['price'],
            'catagory' => $data['catagory'],
            'session' => $data['session'],
            'available' => $data['available'],
        ]);
        dump("test_menu_edit_process: Pass");
    }

    public function test_menu_edit_process_with_negative_price()
    {
        //Prepare Data (including a mock image)
        $product = Product::find(1);
        $testPrice = -999;
        $data = [
            'name' => 'Update Product',
            'description' => 'Update Description',
            'price' => $testPrice,
            'catagory' => $product['catagory'],
            'session' => $product['session'],
            'available' => $product['available'],
            'image' => NULL,
        ];

        $user = $this->authenticate($this->admin);
        $controller = new AdminController();
        $request = new Request($data);
        $response = $controller->menu_edit_process($request, $product['id']);

        $this->assertEquals('Negative Price value do not accept !', session('wrong'));
        $this->assertDatabaseHas('products', [
            'id'=> $product['id'],
            'name' => $product['name'],
            'description' => $product['description'],
            'price' => $product['price'],
            'catagory' => $product['catagory'],
            'session' => $product['session'],
            'available' => $product['available'],
        ]);
        dump("test_menu_edit_process_with_negative_price: Pass");
    }
}
//./vendor/bin/phpunit tests/Unit/MenuControllerTest.php --filter test_menu_edit_process_with_negative_price
